import io
import tkinter as tk
import requests
from PIL import Image, ImageOps, ImageDraw

URL = 'http://127.0.0.1:8000/predict'

class DrawApp:
    def __init__(self, root):
        self.root = root
        root.title('Vẽ chữ số')

        self.canvas = tk.Canvas(root, width=280, height=280, bg='black')
        self.canvas.pack(pady=5)
        self.image = Image.new('L', (280, 280), 0)
        self.draw_image = ImageDraw.Draw(self.image)

        self.last_x = None
        self.last_y = None

        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Button(frame, text='Predict', command=self.predict).pack(side='left', padx=5)
        tk.Button(frame, text='Clear', command=self.clear).pack(side='left', padx=5)
        self.label = tk.Label(root, text='Hãy vẽ 1 con số để tôi đoán!')
        self.label.pack(pady=5)

    def draw(self, event):
        if self.last_x is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width = 18, fill = 'white', capstyle=tk.ROUND, smooth = True)
            self.draw_image.line([self.last_x, self.last_y, event.x, event.y],
                                    fill = 'white', width = 18)
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x = None
        self.last_y = None

    def clear(self):
        self.canvas.delete('all')
        self.draw_image.rectangle([0,0,280,280], fill = 0)
        self.label.config(text='Hãy vẽ 1 con số để tôi đoán!')

    def predict(self):
        buf = io.BytesIO()
        self.image.save(buf, format='PNG')
        buf.seek(0)

        try:
            r = requests.post(URL, files = {'file': ('digit.png', buf, 'image/png')}, timeout=5)
        except requests.exceptions.RequestExeption:
            self.label.config(text='Không kết nối được server!')
            return

        if r.status_code == 200:
            kq = r.json()
            self.label.config(text=f'Dự đoán: {kq['digit']} - Độ tin cậy: {kq['confidence'] * 100:.0f}%')
        else:
            self.label.config(text=f'Lỗi {r.status_code}: {r.json().get('detail', '')}')
                


root = tk.Tk()
app = DrawApp(root)
root.mainloop()

            
