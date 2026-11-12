import io
import numpy as np
import joblib
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image, ImageOps

model = joblib.load('mnist_model.pkl')
app = FastAPI(title='MNIST Digit API')

def preprocess(img):
    arr = np.array(img)
    ys, xs = np.where(arr>20)
    if len(xs) == 0:
        return None
    digit = img.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))

    w,h = digit.size
    scale = 20 / max(w,h)
    nw, nh = max(1, round(w*scale)), max(1, round(h*scale))
    digit = digit.resize((nw, nh), Image.LANCZOS)

    khung = Image.new('L', (28, 28), 0)
    khung.paste(digit, ((28 - nw)//2, (28 - nh)//2))

    a = np.array(khung) / 255.0
    tong = a.sum()
    cy = (a.sum(axis=1) * np.arange(28)).sum() / tong
    cx = (a.sum(axis=0) * np.arange(28)).sum() / tong
    a = np.roll(a, (round(13.5 - cy), round(13.5 - cx)), axis=(0, 1))
    return a.reshape(1, 784)

@app.get('/')
def home():
    return {'message': 'Server đang chạy...'}
@app.post('/predict')
async def predict(file: UploadFile = File(...), invert: bool = False):
    data = await file.read()
    try:
        img = Image.open(io.BytesIO(data)).convert('L')
    except Exception:
      raise HTTPException(status_code=400, detail='File ảnh không hợp lệ!')

    if invert:
        img = ImageOps.invert(img)

    arr = preprocess(img)
    if arr is None:
        raise HTTPException(status_code=400, detail='Ảnh trống! không thấy chữ số')

    xs = model.predict_proba(arr)[0]
    pre = int(xs.argmax())
    return {
        'class': f'chữ số {pre}',
        'digit': pre,
        'confidence': round(float(xs[pre]), 2)
    }
    