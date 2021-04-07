import shutil
from pathlib import Path
import base64
import io
from PIL import Image

from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel



# create FastAPI instance
app = FastAPI()


class ImageBase64(BaseModel):
    base64_str: str


@app.post("/upload_from_image/")
async def predict(token: str = Form(...), file: UploadFile = File(...)):
    print("token:", token)
    filepath = save_upload_file_tmp(file)
    return {'filepath': filepath}


@app.post("/upload_from_base64/")
async def upload_from_base64(image: ImageBase64):
    base64_byte = image.base64_str.encode('utf-8')
    img = decode_img(base64_byte)
    print("img", img.size)
    print('type_image', type(img))
    im1 = img.save("saved/saved_image.jpg")
    return {'img_size': im1}


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        with open("saved/%s"%upload_file.filename, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
    return "/saved/%s"%upload_file.filename

def decode_img(msg):
    msg = msg[msg.find(b"<plain_txt_msg:img>")+len(b"<plain_txt_msg:img>"):
              msg.find(b"<!plain_txt_msg>")]
    msg = base64.b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    print("img", img.size)
    return img

