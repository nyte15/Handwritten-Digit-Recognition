# Nhận diện chữ số viết tay (MNIST + FastAPI + Tkinter)

Ứng dụng cho phép **vẽ một chữ số bằng chuột** và nhận về kết quả dự đoán cùng độ tin cậy.
Dự án được xây dựng theo kiến trúc **client - server**: giao diện Tkinter gửi ảnh lên một REST API (FastAPI), server xử lý ảnh, chạy mô hình Machine Learning và trả kết quả dạng JSON.

## Demo

> ![Demo](demo.png)

## Kiến trúc

```
┌──────────────────┐   POST /predict (ảnh PNG)   ┌────────────────────────────────┐
│  Client          │ ──────────────────────────► │  Server (FastAPI + Uvicorn)    │
│  Tkinter Canvas  │                             │  1. Tiền xử lý ảnh             │
│  (app_client.py) │ ◄────────────────────────── │  2. Logistic Regression        │
└──────────────────┘   JSON: chữ số, độ tin cậy  │  (mnist_api.py)                │
                                                 └────────────────────────────────┘
```

Mô hình chỉ nằm ở server, client không cần cài scikit-learn hay giữ file mô hình.

## Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Mô hình | scikit-learn (Logistic Regression), tập dữ liệu MNIST |
| Xử lý ảnh / số liệu | Pillow, NumPy |
| REST API | FastAPI, Uvicorn, Pydantic |
| Giao diện | Tkinter |
| Gọi API từ client | requests |
| Lưu mô hình | joblib (`.pkl`) |

## Cấu trúc thư mục

```
├── train.py            # Huấn luyện mô hình và lưu mnist_model.pkl
├── test_model.py       # Kiểm tra nhanh mô hình trên ảnh MNIST
├── mnist_model.pkl     # Mô hình đã huấn luyện
├── mnist_api.py        # Server FastAPI (tiền xử lý + dự đoán)
├── app_client.py       # Client Tkinter gọi API
├── app.py              # Phiên bản ban đầu: chạy mô hình trực tiếp, không qua API
├── requirements.txt
└── README.md
```

## Cài đặt

Yêu cầu Python 3.10 trở lên.

```bash
git clone https://github.com/<ten-github>/<ten-repo>.git
cd <ten-repo>
pip install -r requirements.txt
```

(Tùy chọn) Huấn luyện lại mô hình, cần Internet ở lần chạy đầu để tải MNIST:

```bash
python train.py
```

## Cách chạy

### Cách 1: Client - Server (khuyên dùng)

Mở **hai terminal**.

Terminal 1 - chạy server:

```bash
uvicorn mnist_api:app --reload
```

Terminal 2 - chạy giao diện vẽ:

```bash
python app_client.py
```

Vẽ một chữ số lên khung đen (nên vẽ to) rồi bấm **Predict**. Bấm **Clear** để xóa và vẽ lại.

### Cách 2: Bản chạy trực tiếp (không cần server)

```bash
python app.py
```

## REST API

Sau khi chạy server, xem tài liệu và thử API tại: <http://127.0.0.1:8000/docs>

| Method | Đường dẫn | Mô tả |
|---|---|---|
| GET | `/` | Kiểm tra server đang chạy |
| POST | `/predict` | Gửi ảnh chữ số, nhận kết quả dự đoán |

**`POST /predict`**

- Body: `multipart/form-data`, trường `file` là ảnh (PNG/JPG).
- Query (tùy chọn): `invert=true` nếu ảnh là chữ đen nền trắng (mặc định mong đợi chữ trắng nền đen, giống MNIST).

Ví dụ với `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/predict" -F "file=@digit.png"
```

Phản hồi thành công (`200`):

```json
{
  "class": "chữ số 5",
  "digit": 5,
  "confidence": 0.98
}
```

Phản hồi lỗi (`400`), ví dụ file không phải ảnh hoặc ảnh trống:

```json
{ "detail": "Anh trong, khong thay chu so" }
```

## Pipeline xử lý ảnh

Mô hình được huấn luyện trên MNIST (chữ số căn giữa trong khung 28x28), nên ảnh vẽ tay phải được chuẩn hóa giống dữ liệu gốc:

1. Chuyển ảnh sang thang xám.
2. Cắt sát hình chữ nhật bao quanh nét vẽ.
3. Thu/phóng cạnh dài nhất về 20 pixel, giữ nguyên tỉ lệ (bộ lọc LANCZOS).
4. Đặt vào giữa khung 28x28 màu đen.
5. Dịch ảnh để trọng tâm của nét trùng tâm khung.
6. Chia 255 để đưa về khoảng 0-1, duỗi thành vector 784 chiều.

Bước 3-5 giúp kết quả ổn định khi người dùng vẽ nhỏ hoặc lệch khỏi giữa khung.

## Kết quả mô hình

| Mô hình | Độ chính xác trên tập test |
|---|---|
| Logistic Regression | `XX.X%` *(điền số in ra khi chạy `train.py`)* |

## Hạn chế và hướng phát triển

- Logistic Regression không nhận ra hình dạng nét, nên khá nhạy với kiểu chữ viết lạ.
- Dự kiến: so sánh với MLP và CNN, thêm bảng so sánh độ chính xác.
- Dự kiến: hiển thị xác suất của cả 10 chữ số, viết test tự động cho API (pytest), đóng gói bằng Docker.

## Những gì mình học được

- Kiến trúc client - server, REST API (GET/POST, JSON, mã trạng thái HTTP).
- Tách phần suy luận mô hình ra server để nhiều client có thể dùng chung.
- Tiền xử lý dữ liệu phải giống hệt lúc huấn luyện, nếu không kết quả sai dù code không báo lỗi.
- Xử lý lỗi hai phía: API trả `400` rõ ràng, client báo khi không kết nối được server.
