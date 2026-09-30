# SecureCrypto

SecureCrypto là toolkit Python cho một số thao tác mật mã cơ bản: mã hóa tệp bằng AES-GCM, băm mật khẩu với Argon2, tạo chữ ký RSA và kiểm tra chữ ký. Dự án cung cấp CLI, giao diện desktop Tkinter và API HTTP Flask.

> Đây là dự án học tập, chưa được đánh giá bảo mật độc lập. Không dùng API Flask trực tiếp trên Internet hoặc để bảo vệ dữ liệu quan trọng.
> 
<img width="1917" height="1078" alt="Screenshot 2026-09-30 205839" src="https://github.com/user-attachments/assets/0eaa8617-2dc4-471d-95d0-7888d9b88d1f" />

## Tính năng


- Mã hóa và giải mã tệp bằng AES-GCM; khóa được dẫn xuất từ mật khẩu qua PBKDF2-HMAC-SHA256.
- Băm mật khẩu bằng Argon2.
- Tạo cặp khóa RSA 2048-bit, ký dữ liệu với SHA-256 và xác minh chữ ký.
- Sử dụng chức năng mã hóa/giải mã tệp từ CLI, Tkinter GUI hoặc Flask API.
<img width="1917" height="1078" alt="Screenshot 2026-09-30 210114" src="https://github.com/user-attachments/assets/01634ad2-ae03-453e-85bb-3b75e4dbb707" />

## Yêu cầu

- Python 3.8 trở lên.
- Tkinter nếu sử dụng giao diện desktop (thường có sẵn với Python trên Windows).

## Cài đặt

Mở terminal tại thư mục `crypto-toolkit`, sau đó chạy:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -r requirements.txt
```

Lệnh cài đặt editable lấy các thư viện runtime được khai báo trong `setup.py`; `requirements.txt` cài thêm pytest để chạy kiểm thử.

## Sử dụng

### CLI

Mã hóa một tệp:

```powershell
securecrypto-cli --encrypt files/data.txt --password "mat-khau-cua-ban"
```

Lệnh tạo `files/data.txt.enc` và in ra khóa AES dạng Base64. Lưu khóa này ở nơi an toàn. Để giải mã, truyền khóa Base64 vừa nhận vào tùy chọn `--password`:

```powershell
securecrypto-cli --decrypt files/data.txt.enc --password "KHOA_AES_BASE64"
```

Tệp giải mã được ghi thành `files/data.txt.dec`.

### Giao diện desktop

```powershell
python -m securecrypto.app_gui
```

Chọn tệp và nhập mật khẩu để mã hóa. Khi giải mã, nhập khóa Base64 được in ra lúc mã hóa vào ô mật khẩu.

### Flask API

Khởi chạy máy chủ phát triển:

```powershell
python -m securecrypto.api
```

Máy chủ mặc định chạy tại `http://127.0.0.1:5000`. Cả hai endpoint nhận multipart form gồm tệp `file` và trường văn bản `password`:

- `POST /encrypt`: mã hóa tệp, trả về JSON như `{"key": "KHOA_AES_BASE64"}`.
- `POST /decrypt`: giải mã tệp; trường `password` phải chứa khóa Base64 từ bước mã hóa. Trả về JSON có đường dẫn tệp đầu ra.

Ví dụ gọi endpoint mã hóa bằng `curl.exe`:

```powershell
curl.exe -X POST -F "file=@files/data.txt" -F "password=mat-khau-cua-ban" http://127.0.0.1:5000/encrypt
```

API hiện chưa có xác thực, giới hạn kích thước tải lên hay xử lý tên tệp an toàn; chỉ nên chạy cục bộ để thử nghiệm.

## Dùng thư viện Python

```python
from securecrypto import aes_utils, hash_utils, rsa_utils

# Băm mật khẩu
password_hash = hash_utils.hash_password_secure("mat-khau")

# Tạo khóa RSA và ký dữ liệu
private_key, public_key = rsa_utils.generate_rsa_keypair()
message = b"Du lieu can ky"
signature = rsa_utils.sign_data_rsa(message, private_key)
is_valid = rsa_utils.verify_signature_rsa(message, signature, public_key)
```

`verify_signature_rsa` trả về `True` nếu chữ ký hợp lệ, ngược lại trả về `False`. Hàm băm trả về chuỗi Argon2; có thể xác minh chuỗi này bằng `PasswordHasher.verify` từ thư viện `argon2-cffi`.

## Chạy kiểm thử

```powershell
python -m pytest
```

Các test hiện có kiểm tra vòng đời mã hóa/giải mã tệp, băm mật khẩu và tạo/xác minh chữ ký RSA.

## Lưu ý về khóa AES

Trong phiên bản hiện tại, `encrypt_file_aes` nhận mật khẩu, dẫn xuất khóa bằng PBKDF2-HMAC-SHA256 với 100.000 vòng lặp rồi trả khóa dưới dạng Base64. Tuy nhiên, `decrypt_file_aes` nhận trực tiếp khóa Base64, không tự dẫn xuất khóa từ mật khẩu. Vì vậy cần giữ khóa được trả về lúc mã hóa để giải mã; chỉ nhớ mật khẩu ban đầu là chưa đủ. Tên tham số `--password` và trường `password` ở các giao diện giải mã hiện chưa phản ánh chính xác điều này.
