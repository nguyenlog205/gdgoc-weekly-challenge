# Tuần 01 - Bài tập tuần 0 - 1

> Đề bài: [Tuần 0 + 1: GDGoC-UIT (AI Team): Task 1](https://eight-drip-1cb.notion.site/Tu-n-0-1-GDGoC-UIT-AI-Team-Task-1-2a439f5e0c9a801088a0f35cf54f4d8a)

## Cấu Trúc Dự Án
```
week-01/
├── README.md          # README mô tả bài nộp
├── requirements.txt   # Danh sách thư viện Python cần thiết
├── notebook/         
│   └── report.ipynb  # Bài làm
└── src/              # Thư mục chứa mã nguồn liên quan
    │── __init__.py
    │── analyze_univariate.py  # Mã nguồn để phân tích đơn biến
    │── calculate_corr_matrix.py # Tính toán ma trận tương quan và p-value
    └── extract_general_description.py # Trích xuất mô tả chung về dữ liệu
```

## Hướng Dẫn Cài Đặt

1. Tạo môi trường ảo (khuyến nghị):
```bash
python -m venv venv
source venv/bin/activate  # Cho Linux/Mac
.\venv\Scripts\activate   # Cho Windows
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Tổng Quan Dự Án
Thư mục này chứa bài tập thử thách của tuần đầu tiên, tập trung vào phân tích dữ liệu sử dụng Python. Phần chính của bài tập và phân tích có thể được tìm thấy trong Jupyter notebook tại đường dẫn `notebook/report.ipynb`.

### Mô Tả Thư Mục
- `notebook/`: Chứa các Jupyter notebook để phân tích và trực quan hóa dữ liệu
- `src/`: Chứa các script và module Python hỗ trợ
- `requirements.txt`: Liệt kê tất cả các thư viện Python cần thiết

