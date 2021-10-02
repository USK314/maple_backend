from fastapi import UploadFile, HTTPException, status
import os
from uuid import uuid4
from firebase import bucket
from firebase import db
from firebase_admin import firestore
import compression


tmp_dir_name = "/tmp" if os.environ.get("DYNO") else "./tmp"


async def save_tmp(file: UploadFile) -> str:
    filename = str(uuid4())
    _, ext = os.path.splitext(file.filename)
    tmp_path = os.path.join(tmp_dir_name, f"{filename}{ext}")
    fout = open(tmp_path, 'wb')
    while True:
        chunk = await file.read(100000)
        if not chunk:
            break
        fout.write(chunk)
    fout.close()
    return tmp_path, filename, ext


async def save_file_to_cloud_storage(tmp_path: str, filename: str, ext: str) -> str:
    # storage にアップロードする
    blob = bucket.blob(f"{filename}{ext}")
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token}
    blob.metadata = metadata
    blob.upload_from_filename(tmp_path)
    blob.make_public()
    public_url = blob.public_url
    return public_url


async def get_all_posts():
    docs = db.collection("posts").stream()
    data = []
    for doc in docs:
        post = {"id": doc.id, **doc.to_dict()}
        data.append(post)
    return data


async def get_new_posts():
    docs = db.collection("posts")
    query = docs.order_by(
        "createdAt", direction=firestore.Query.DESCENDING).limit(5)
    results = query.stream()
    data = []
    for doc in results:
        post = {"id": doc.id, **doc.to_dict()}
        data.append(post)
    return data


async def create_post(comment: str, lat: float, lng: float, image: UploadFile, genre: str = "default"):
    if not (image.content_type == "image/png" or image.content_type == "image/jpeg"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="\"image/png\" or \"image/jpeg\" のみ受け付けます")
    tmp_path, filename, ext = await save_tmp(image)
    # TODO: 保存する前に圧縮
    compressed_path = compression.compress(tmp_path, image.content_type)
    # TODO: そして画像認識
    public_url = await save_file_to_cloud_storage(compressed_path, filename, ext)
    os.remove(compressed_path)
    doc_ref = db.collection('posts').document()
    doc_ref.set({
        'imagePath': public_url,
        'comment': comment,
        'lat': lat,
        'lng': lng,
        'genre': genre,
        'favorites': 0,
        'createdAt': firestore.SERVER_TIMESTAMP,
    })
    return True


async def favorite_to_post(post_id: str):
    doc_ref = db.collection("posts").document(post_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="投稿が見つかりませんでした")
    data = doc.to_dict()
    current_favorites = data["favorites"]
    # それを更新する
    doc_ref.set({"favorites": current_favorites + 1}, merge=True)
