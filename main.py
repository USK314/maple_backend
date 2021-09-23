from fastapi import FastAPI, Depends, File, UploadFile, Form, status
from fastapi.responses import JSONResponse
import uvicorn
from sqlalchemy.orm import Session
import crud
import models
from database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
from typing import List, Optional

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

cred = credentials.Certificate("cert.json")

firebase_admin.initialize_app(cred, {
    'storageBucket': 'garigari-stagram.appspot.com',
    'projectId': 'garigari-stagram',
})

bucket = storage.bucket()
db = firestore.client()

# TODO: cloud storage との接続
# TODO: firestore との接続
# TODO: 実装

app = FastAPI()

app.mount("/static", StaticFiles(directory="uploads"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "this is root"}


@app.get("/posts")
async def posts(db: Session = Depends(get_db)):
    posts = crud.get_all_posts(db)
    return {"message": "get all posts here", "data": posts}


@app.post("/post")
async def post(
    garigari_name: str = Form(...),
    comment: Optional[str] = None,
    lat: float = Form(...),
    lng: float = Form(...),
    image: UploadFile = File(...),
    genre: str = Form(...),
    db: Session = Depends(get_db)
):
    await crud.create_post(db, garigari_name, comment, lat, lng, image, genre)
    return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_201_CREATED)


@app.post("/favorite")
async def favorite():
    return {"message": "this is favorite"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
