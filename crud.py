from fastapi import UploadFile, HTTPException
import os
import uuid
import datetime
from sqlalchemy.orm import Session

# タスク
# - 保存のところをちょっと変える→@takapiro99
# - herokuにデプロイ
# - githubとherokuのやつをslack又はdiscordと連携

tmp_dir_name = "/tmp" if os.environ.get("DYNO") else "./tmp"


async def save_file(file: UploadFile) -> str:
    """
    file を受け取って保存しにいってくれるくん
    pathを返す
    """
    if file.content_type == "image/png" or file.content_type == "image/jpeg":
        filename = str(uuid.uuid4())
        _, ext = os.path.splitext(file.filename)
        path = os.path.join(tmp_dir_name, f"{filename}{ext}")
        # TODO: print はしない
        print(path)
        fout = open(path, 'wb')
        while True:
            chunk = await file.read(100000)
            if not chunk:
                break
            fout.write(chunk)
        fout.close()
        return path
    else:
        raise HTTPException(
            status_code=422, detail="\"image/png\" or \"image/jpeg\" のみ受け付けます")


def get_all_posts():
    # TODO: 実装
    return []


async def create_post(db, garigari_name: str, comment: str, lat: float, lng: float, image: UploadFile, genre: str):
    tmp_path = await save_file(image)
    print(tmp_path)
    # TODO: cloud storage に upload
    os.remove(tmp_path)
    # TODO: 実装
    return True
