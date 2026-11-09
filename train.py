from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

x, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)
x = x / 255.0
y = y.astype(int)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)

print(model.score(x_test, y_test))
joblib.dump(model, 'mnist_model.pkl')
print("Saved")
