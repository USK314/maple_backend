from fastapi import FastAPI, Depends, File, UploadFile, Form, status
from fastapi.responses import JSONResponse
import uvicorn
from sqlalchemy.orm import Session
import crud
from fastapi.staticfiles import StaticFiles
from typing import List, Optional

from firebase import bucket, db

print(bucket, db)
# TODO: cloud storage との連携
# TODO: firestore との連携
# TODO: 実装

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "this is root"}


@app.get("/posts")
async def posts():
    # posts = crud.get_all_posts(db)
    posts = []
    return {"message": "get all posts here", "data": posts}


@app.post("/post")
async def post(
    garigari_name: str = Form(...),
    comment: Optional[str] = None,
    lat: float = Form(...),
    lng: float = Form(...),
    image: UploadFile = File(...),
    genre: str = Form(...),
):
    await crud.create_post(None, garigari_name, comment, lat, lng, image, genre)
    return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_201_CREATED)


@app.post("/favorite")
async def favorite():
    return {"message": "this is favorite"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
