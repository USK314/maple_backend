from fastapi import FastAPI, File, UploadFile, Form, status
from fastapi.responses import JSONResponse
import uvicorn
import crud
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost",
    # TODO: フロントエンドデプロイしたらそのURLも入れる
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "this is root"}


@app.get("/posts")
async def posts():
    posts = await crud.get_all_posts()
    resp = {
        "status": "ok",
        "count": len(posts),
        "data": posts
    }
    return resp


@app.post("/post")
async def post(
    garigari_name: str = Form(...),
    comment: Optional[str] = None,
    lat: float = Form(...),
    lng: float = Form(...),
    image: UploadFile = File(...),
    genre: str = Form(...),
):
    await crud.create_post(garigari_name, comment, lat, lng, image, genre)
    return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_201_CREATED)


@app.post("/favorite")
async def favorite(post_id: str):
    await crud.favorite_to_post(post_id)
    return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_204_NO_CONTENT)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
