from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
from yolo1 import detect_and_track
import io

app = FastAPI()

@app.post("/track/")
async def track_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    output_img = detect_and_track(img)

    _, img_encoded = cv2.imencode('.jpg', output_img)
    return StreamingResponse(io.BytesIO(img_encoded.tobytes()), media_type="image/jpeg")
