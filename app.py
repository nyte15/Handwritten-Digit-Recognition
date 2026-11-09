import tkinter as tk
import numpy as np
import joblib
from PIL import Image, ImageDraw

model = joblib.load('mnist_model.pkl')

class DrawApp:
    def __init__(self, root):
        self.root = root
        root.title('Ve chu so')

        self.canvas = tk.Canvas(root, width = 280, height= 280, bg = 'black')
        self.canvas.pack(pady=5)

        self.image = Image.new('L', (280, 280), 0)
        self.draw_img = ImageDraw.Draw(self.image)

        self.last_x = None
        self.last_y = None

        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Button(frame, text='Predict', command=self.predict).pack(side='left', padx=5)
        tk.Button(frame, text='Clear', command=self.clear).pack(side='left', padx=5)
        self.lable = tk.Label(root, text="Hãy vẽ một con số để tôi đoán!")
        self.lable.pack(pady=5)

    def draw(self, event):
        if self.last_x is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=18, fill='white', capstyle=tk.ROUND, smooth=True)
            self.draw_img.line(
                [self.last_x, self.last_y, event.x, event.y],
                fill=255, width=18
            )
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x = None
        self.last_y = None

    def clear(self):
        self.canvas.delete('all')
        self.draw_img.rectangle([0,0,280,280], fill=0)
        self.lable.config(text='Hãy vẽ một con số để tôi đoán!')

    def predict(self):
        img = self.image.resize((28, 28), Image.LANCZOS)
        arr = np.array(img) / 255.0
        arr = arr.reshape(1, 784)
        pre = model.predict(arr)[0]
        do_tin_cay = model.predict_proba(arr).max() * 100
        self.lable.config(text=f'Predict: {pre} - Độ tin cậy là: {do_tin_cay:.0f}%')

root = tk.Tk()
app = DrawApp(root)
root.mainloop()