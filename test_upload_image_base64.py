import json
import requests
import base64
import io
from PIL import Image

def img_to_txt(filename):
    msg = b"<plain_txt_msg:img>"
    with open(filename, "rb") as imageFile:
        msg = msg + base64.b64encode(imageFile.read())
    msg = msg + b"<!plain_txt_msg>"
    return msg

def decode_img(msg):
    msg = msg[msg.find(b"<plain_txt_msg:img>")+len(b"<plain_txt_msg:img>"):
              msg.find(b"<!plain_txt_msg>")]
    msg = base64.b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    print("img", img.size)
    return img


def test_show_image():
    filename = 'download.jpeg'
    msg = img_to_txt(filename)
    img = decode_img(msg)
    img.show()


def upload_from_base64(image_file, url):
    data = {'base64_str': img_to_txt(image_file).decode("utf-8")}
    response = requests.post(url, data=json.dumps(data))
    #response = requests.post(url, data=data)
    print(response.text)
    return response.text


# endpoint for predict from base64
predict_url_base64 = 'http://localhost:8000/upload_from_base64/'

# send predict request
label = upload_from_base64('download.jpeg', predict_url_base64)
