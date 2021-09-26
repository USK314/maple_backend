from fastapi import UploadFile, HTTPException
import os
from uuid import uuid4
from firebase import bucket
from firebase import db
from firebase_admin import firestore


tmp_dir_name = "/tmp" if os.environ.get("DYNO") else "./tmp"


async def save_file_to_cloud_storage(file: UploadFile) -> str:
    """
    file を受け取って保存しにいってくれるくん
    path を返す
    """
    if file.content_type == "image/png" or file.content_type == "image/jpeg":
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
        # storage にアップロードする
        blob = bucket.blob(f"{filename}{ext}")
        new_token = uuid4()
        metadata = {"firebaseStorageDownloadTokens": new_token}
        blob.metadata = metadata
        blob.upload_from_filename(tmp_path)
        blob.make_public()
        public_url = blob.public_url
        os.remove(tmp_path)
        return public_url
    else:
        raise HTTPException(
            status_code=422, detail="\"image/png\" or \"image/jpeg\" のみ受け付けます")


async def get_all_posts():
    docs = db.collection("posts").stream()
    data = []
    for doc in docs:
        post = {"id": doc.id, **doc.to_dict()}
        data.append(post)
    return data


async def create_post(garigari_name: str, comment: str, lat: float, lng: float, image: UploadFile, genre: str):
    public_url = await save_file_to_cloud_storage(image)
    doc_ref = db.collection('posts').document()
    doc_ref.set({
        'garigariName': garigari_name,
        'imagePath': public_url,
        'comment': comment,
        'lat': lat,
        'lng': lng,
        'genre': genre,
        'favorites': 0,
        'createdAt': firestore.SERVER_TIMESTAMP,
    })
    return True
