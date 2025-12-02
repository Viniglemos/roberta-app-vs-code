from typing import List, Optional
from datetime import datetime
import mimetypes

from fastapi import FastAPI, HTTPException, status, Depends, UploadFile, File
from pydantic import BaseModel, EmailStr
from bson import ObjectId

from src.utils.db import clients_collection, albums_collection, photos_collection
from src.utils.auth import get_api_key
from src.utils.s3 import upload_fileobj_to_s3, generate_presigned_url

app = FastAPI()

# ====== MODELS ======

class Client(BaseModel):
    name: str
    email: EmailStr  # validates email format automatically

class Album(BaseModel):
    title: "str"
    client_name: str
    event_date: str  # string for now (easier)
    tags: List[str] = []

# ====== HELPERS TO CLEAN MONGODB DOCUMENTS ======

def client_from_mongo(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
    }

def album_from_mongo(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "client_name": doc["client_name"],
        "event_date": doc["event_date"],
        "tags": doc.get("tags", []),
    }

def photo_from_mongo(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "album_id": str(doc["album_id"]),
        "s3_key": doc["s3_key"],
        "url": generate_presigned_url(doc["s3_key"]),
        "description": doc.get("description"),
        "uploaded_at": doc.get("uploaded_at"),
    }

# ====== ROOT / HEALTH ======

@app.get("/")
def read_root():
    return {"message": "Backend is running with MongoDB & Docker!"}

@app.get("/hello")
def say_hello():
    return {"message": "Hello, Vinicius! Your API is working :)"}

# ====== CLIENTS ======


@app.post("/clients")
def create_client(client: Client, api_key: str = Depends(get_api_key)):
    """
    Create a client, but:
    - reject if email is already registered
    """
    existing = clients_collection.find_one({"email": client.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A client with this email already exists.",
        )

    result = clients_collection.insert_one(client.dict())
    created = clients_collection.find_one({"_id": result.inserted_id})
    return {
        "message": "Client added successfully",
        "client": client_from_mongo(created),
    }


@app.get("/clients")
def get_clients():
    docs = clients_collection.find()
    return [client_from_mongo(doc) for doc in docs]


# ====== ALBUMS ======


@app.post("/albums")
def create_album(album: Album, api_key: str = Depends(get_api_key)):
    """
    Create an album, but:
    - check if the client exists (by name)
    """
    client = clients_collection.find_one({"name": album.client_name})
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client '{album.client_name}' not found. Create the client first.",
        )

    result = albums_collection.insert_one(album.dict())
    created = albums_collection.find_one({"_id": result.inserted_id})
    return {
        "message": "Album created successfully",
        "album": album_from_mongo(created),
    }


@app.get("/albums")
def get_albums():
    docs = albums_collection.find()
    return [album_from_mongo(doc) for doc in docs]


@app.get("/albums/by_tag")
def get_albums_by_tag(tag: str):
    docs = albums_collection.find({"tags": tag})
    return [album_from_mongo(doc) for doc in docs]

@app.get("/albums/by_client")
def get_albums_by_client(client_name: str):
    """
    New helper endpoint: list all albums for a specific client
    """
    docs = albums_collection.find({"client_name": client_name})
    return [album_from_mongo(doc) for doc in docs]


# ====== PHOTOS (S3) ======

@app.post("/albums/{album_id}/photos")
async def upload_photo_to_album(
    album_id: str,
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key),
):
    """
    Upload a photo to S3 and register it in Mongo, linked to an album.
    """
    # 1) Check if album exists
    try:
        album_obj_id = ObjectId(album_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid album_id",
        )

    album = albums_collection.find_one({"_id": album_obj_id})
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found",
        )

    # 2) Build S3 key
    filename = file.filename or "photo.jpg"
    content_type = file.content_type or mimetypes.guess_type(filename)[0] or "image/jpeg"

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    s3_key = f"albums/{album_id}/{timestamp}_{filename}"

    # 3) Upload to S3
    try:
        upload_fileobj_to_s3(file.file, key=s3_key, content_type=content_type)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload to S3: {exc}",
        )

    # 4) Save photo metadata in Mongo
    photo_doc = {
        "album_id": album_obj_id,
        "s3_key": s3_key,
        "uploaded_at": datetime.utcnow(),
    }
    result = photos_collection.insert_one(photo_doc)
    created = photos_collection.find_one({"_id": result.inserted_id})

    return {
        "message": "Photo uploaded successfully",
        "photo": photo_from_mongo(created),
    }

@app.get("/albums/{album_id}/photos")
def list_photos_for_album(album_id: str):
    """
    List photos for a given album, each with a presigned S3 URL.
    """
    try:
        album_obj_id = ObjectId(album_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid album_id",
        )

    album = albums_collection.find_one({"_id": album_obj_id})
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found",
        )

    docs = photos_collection.find({"album_id": album_obj_id})
    return [photo_from_mongo(doc) for doc in docs]

# ====== SIMPLE TEST UPLOAD (no S3, no Mongo) ======


@app.post("/test-upload-no-s3")
async def test_upload_no_s3(file: UploadFile = File(...)):
    return {"filename": file.filename}
