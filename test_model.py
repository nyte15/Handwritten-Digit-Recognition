from sklearn.datasets import fetch_openml
import joblib

model = joblib.load('mnist_model.pkl')

x,y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)
x = x / 255.0
y = y.astype(int)

for i in range(-5, 0):
    anh = x[i].reshape(1,-1)
    pre = model.predict(anh)[0]
    print(f'Du doan: {pre} | Thuc te: {y[i]}')