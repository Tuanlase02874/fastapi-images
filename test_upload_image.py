import json
import requests
from base64 import b64encode
from io import BytesIO
from PIL import Image


def predict_from_image(filename, url):
    files = [('file', open(filename, 'rb'))]
    response = requests.post(url, files=files)
    label = json.loads(response.text)['label']

    return label

# endpoint for predict from image
predict_url_image = 'http://localhost:8000/upload_from_image/'

# send predict request
label = predict_from_image('download.jpeg', predict_url_image)
