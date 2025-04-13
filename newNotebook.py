import pandas as pd
import numpy as np


def hi():
    print("hello, world")

if __name__ == "__main__":
    hi()



import io
import pandas as pd
from b2sdk.v2 import B2Api, InMemoryAccountInfo

KEY_ID = 'b68f92eeb725'  # Thay bằng Key ID của bạn
APPLICATION_KEY = '00522b8989b6e76142932d27b7e6036de5232f3025' # Thay bằng Application Key của bạn
BUCKET_NAME = 'ThanhDZ2503' # Tên bucket của bạn
FILE_NAME = 'between.xlsx' # Tên file trong bucket

# --- Khởi tạo thông tin tài khoản và API ---
print("Đang khởi tạo thông tin tài khoản B2...")
info = InMemoryAccountInfo()
b2_api = B2Api(info)

# --- Xác thực ---
print(f"Đang xác thực với Key ID: {KEY_ID[:5]}...") # Chỉ in một phần key ID cho an toàn
try:
    b2_api.authorize_account("production", KEY_ID, APPLICATION_KEY)
    account_id = b2_api.account_info.get_account_id()
    print(f"Xác thực thành công! Account ID: {account_id}")
except Exception as e:
    print(f"Lỗi xác thực: {e}")
    # Thoát nếu không xác thực được
    exit()

# --- Lấy thông tin bucket ---
print(f"Đang lấy thông tin bucket '{BUCKET_NAME}'...")
try:
    bucket = b2_api.get_bucket_by_name(BUCKET_NAME)
    print(f"Tìm thấy bucket '{BUCKET_NAME}'.")
except Exception as e:
    print(f"Lỗi khi lấy thông tin bucket '{BUCKET_NAME}': {e}")
    # Thoát nếu không tìm thấy bucket
    exit()

# --- Tải file vào bộ nhớ ---
print(f"Đang tải file '{FILE_NAME}' từ bucket '{BUCKET_NAME}'...")
try:
    # Tạo một đối tượng BytesIO để lưu dữ liệu file tải về
    file_content = io.BytesIO()
    
    # Tải file
    downloaded_file = bucket.download_file_by_name(FILE_NAME)
    downloaded_file.save(file_content)
    
    # Đưa con trỏ về đầu stream để pandas có thể đọc
    file_content.seek(0)
    
    print(f"Tải file '{FILE_NAME}' thành công.")

    # --- Đọc file Excel bằng Pandas ---
    print("Đang đọc nội dung file Excel...")
    # Sử dụng pandas để đọc dữ liệu từ đối tượng BytesIO trong bộ nhớ
    # Mặc định pandas sử dụng openpyxl, bạn có thể cần cài nó
    excel_data = pd.read_excel(file_content) # Bạn có thể thêm các tham số như sheet_name='Sheet1' nếu cần

    # --- Hiển thị dữ liệu (ví dụ: 5 dòng đầu) ---
    print("\nNội dung file Excel (5 dòng đầu):")
    print("excel_data.head()")

    # Bạn có thể thực hiện các thao tác khác với 'excel_data' ở đây
    # Ví dụ: print(excel_data.info()) hoặc print(excel_data)

except Exception as e:
    print(f"Lỗi trong quá trình tải hoặc đọc file '{FILE_NAME}': {e}")

print("\nHoàn tất.")

# --- Kết thúc ---

print("Kết thúc chương trình.")
# Bạn có thể thêm các thao tác khác ở đây nếu cần