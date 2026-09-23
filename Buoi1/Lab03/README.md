# Lab 03 - Xây dựng hệ thống logging bảo mật và kiểm tra đầu vào an toàn

## 1. Thông tin bài làm

- Môn học: Thực hành Lập trình An ninh thông tin
- Bài: Lab 03 - Thiết kế logger an toàn và ghi nhận sự kiện kiểm tra dữ liệu đầu vào
- Ứng dụng: Flask API + module validate + module logging an toàn
- Công nghệ: Python, Flask, logging, JSON, hashlib, gzip

## 2. Mục tiêu

Lab 03 tập trung vào việc xây dựng một hệ thống logging bảo mật cho ứng dụng web. Mục tiêu chính của bài làm là:

1. Kiểm tra đầu vào từ người dùng theo các tiêu chí an ninh cơ bản.
2. Ghi log sự kiện dưới dạng JSON để dễ quản lý và phân tích.
3. Mask hoặc ẩn dữ liệu cá nhân nhạy cảm trước khi lưu vào file log.
4. Tạo chữ ký hash cho từng dòng log để phát hiện thay đổi hoặc chỉnh sửa log.
5. Tự động rotate và nén file log để giảm nguy cơ mất dữ liệu và tiết kiệm dung lượng.

## 3. Cấu trúc thư mục

```text
Lab03/
|-- app.py                       # Ứng dụng Flask API nhận JSON và thực hiện kiểm tra
|-- requirements.txt             # Danh sách thư viện cần cài đặt
|-- secure.log                   # File log JSON lưu trữ các sự kiện
|-- secure.log.sig               # File lưu hash chữ ký từng dòng log
|-- securevalidator/
|   |-- __init__.py              # Khởi tạo package
|   `-- core.py                  # Hàm validate_email, validate_url, validate_filename, sanitize_sql_input, sanitize_html_input
|-- securelogger/
|   |-- __init__.py              # Khởi tạo package logger
|   `-- logger.py                # Module logging an toàn, masking dữ liệu PII và chia nhỏ log
`-- README.md                    # Báo cáo bài làm
```

## 4. Mô tả chức năng hệ thống

### 4.1. API validate

Ứng dụng Flask cung cấp endpoint `/validate` với phương thức `POST`.

Khi client gửi dữ liệu JSON, server sẽ:

- kiểm tra định dạng JSON;
- đọc các trường `email`, `url`, `filename`, `sql`, `html`;
- gọi các hàm validator tương ứng;
- ghi log lại dữ liệu đầu vào và kết quả kiểm tra.

Ví dụ payload:

```json
{
  "email": "user@example.com",
  "url": "https://example.com",
  "filename": "report.pdf",
  "sql": "SELECT * FROM users",
  "html": "<script>alert('xss')</script>"
}
```

### 4.2. Các hàm kiểm tra đầu vào

File `securevalidator/core.py` bao gồm các hàm sau:

#### a) `validate_email(email)`
- Kiểm tra định dạng email bằng regex.
- Chỉ chấp nhận chuỗi có dạng cơ bản: `name@domain.com`
- Trả về `True` nếu hợp lệ, `False` nếu không.

#### b) `validate_url(url)`
- Phân tích URL bằng `urllib.parse.urlparse()`.
- Chỉ chấp nhận scheme `http` hoặc `https` và có `netloc`.
- Ngăn chặn một số dạng URL không hợp lệ hoặc dễ bị lạm dụng.

#### c) `validate_filename(filename)`
- Chặn path traversal: `..`, `/`, `\\`
- Đảm bảo filename chỉ là tên file đơn thuần, không phải đường dẫn.

#### d) `sanitize_sql_input(input_str)`
- Xóa các ký tự nguy hiểm như `--`, `;`, dấu nháy đơn, dấu nháy kép, `#`.
- Loại bỏ từ khóa SQL phổ biến như `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `DROP`, `UNION`, `WHERE`, `OR`, `AND`.

#### e) `sanitize_html_input(html_str)`
- Dùng `html.escape()` để mã hóa ký tự HTML.
- Ngăn chặn XSS khi hiển thị dữ liệu trên giao diện.

## 5. Hệ thống logging an toàn

Module `securelogger/logger.py` được xây dựng để lưu log an toàn hơn so với logging mặc định của Python.

### 5.1. Masking dữ liệu nhạy cảm

Hệ thống định nghĩa các pattern để phát hiện và thay thế dữ liệu nhạy cảm:

- email
- token
- API key
- password

Ví dụ:

```text
"email": "user@example.com"
```

sẽ được ghi lại thành:

```text
"<email_masked>"
```

Điều này giúp tránh việc lưu thông tin riêng tư trực tiếp trong file log.

### 5.2. Định dạng JSON cho log

Mỗi dòng log được ghi dưới dạng JSON, gồm các trường:

- `timestamp`
- `level`
- `message`
- `data` (nếu có)
- `results` (nếu có)

Ví dụ:

```json
{
  "timestamp": "2026-09-23T08:00:00Z",
  "level": "INFO",
  "message": "Validation check performed",
  "data": {"email": "<email_masked>", "url": "https://example.com"},
  "results": {"email": true, "url": true}
}
```

### 5.3. Chữ ký log

Mỗi dòng log khi ghi xuống file sẽ được băm bằng SHA-256 và lưu vào `secure.log.sig`.

Cách làm này giúp:

- phát hiện log bị chỉnh sửa;
- truy vết dữ liệu bị thay đổi;
- tăng tính toàn vẹn và bảo mật của file log.

### 5.4. Rotate và nén log

Logger sử dụng `RotatingFileHandler` để giới hạn kích thước file log lên tới `1MB`. Khi file lớn quá mức cho phép, hệ thống sẽ:

- tạo file backup mới;
- nén file cũ bằng gzip;
- xoá log gốc cũ để tiết kiệm dung lượng.

## 6. Luồng xử lý ứng dụng

1. Client gửi request `POST /validate` với JSON.
2. Flask đọc dữ liệu đầu vào bằng `request.get_json(force=True)`.
3. Nếu JSON không hợp lệ, hệ thống ghi cảnh báo log và trả về lỗi `400`.
4. Mỗi trường dữ liệu được kiểm tra bằng validator tương ứng.
5. Kết quả kiểm tra được lưu vào `results`.
6. Logger ghi một sự kiện `INFO` với dữ liệu đầu vào và kết quả đánh giá.
7. Dữ liệu nhạy cảm trong log được mask trước khi lưu.
8. Log được ký hash và lưu vào `secure.log.sig`.

## 7. Cài đặt và chạy ứng dụng

### 7.1. Tạo môi trường ảo

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 7.2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 7.3. Chạy ứng dụng

```bash
python app.py
```

Ứng dụng sẽ chạy ở địa chỉ:

```text
http://127.0.0.1:5000/validate
```

## 8. Ví dụ kiểm thử

Gửi request POST bằng `curl`:

```bash
curl -X POST http://127.0.0.1:5000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "url": "https://example.com",
    "filename": "test.pdf",
    "sql": "SELECT * FROM users WHERE id = 1",
    "html": "<script>alert(1)</script>"
  }'
```

Kết quả trả về sẽ có dạng:

```json
{
  "email": true,
  "url": true,
  "filename": true,
  "sql": "* FROM users WHERE id = 1",
  "html": "&lt;script&gt;alert(1)&lt;/script&gt;"
}
```

## 9. Kết quả đạt được

Sau khi hoàn thành Lab 03, hệ thống đã đạt được các yêu cầu sau:

- kiểm tra đầu vào cơ bản an toàn;
- hạn chế tấn công XSS, SQL injection, path traversal, SSRF cơ bản;
- lưu log theo định dạng JSON chuyên nghiệp;
- ẩn dữ liệu cá nhân nhạy cảm trong log;
- tạo chữ ký để kiểm tra tính toàn vẹn của log;
- rotate và nén log tự động.

## 10. Đánh giá bảo mật và hạn chế

### Ưu điểm

- Tích hợp kiểm tra bảo mật ngay trong ứng dụng API.
- Log dễ mở rộng và dễ phân tích.
- Mask PII giúp giảm rủi ro rò rỉ thông tin.
- Chữ ký hash cho phép phát hiện truy cập bất hợp pháp hoặc chỉnh sửa log.

### Hạn chế

- Regex kiểm tra dữ liệu nhạy cảm chỉ là cơ chế mẫu, chưa phải giải pháp bảo mật hoàn chỉnh.
- Kiểm tra đầu vào do lab thực hiện mới ở mức cơ bản, chưa đủ cho hệ thống production.
- Rotation và nén log cần được quản lý cẩn thận để không làm mất dữ liệu quan trọng trong môi trường lớn.

## 11. Kết luận

Lab 03 đã giúp hiểu rõ hơn cách xây dựng một ứng dụng web vừa có chức năng kiểm tra đầu vào vừa đảm bảo ghi log an toàn. Việc kết hợp giữa validation và secure logging là một phần rất quan trọng trong chính sách bảo mật ứng dụng, bởi vì một hệ thống an toàn không chỉ cần chặn tấn công mà còn cần theo dõi, ghi nhận và phát hiện các sự kiện bất thường.

Qua bài làm này, tôi đã nắm được cách:

- kiểm tra đầu vào từ người dùng;
- giảm thiểu rủi ro XSS, SQLi, path traversal và SSRF cơ bản;
- lưu log theo chuẩn JSON;
- bảo vệ log bằng masking và hash signature;
- triển khai cơ chế rotate log để quản lý tài nguyên hiệu quả hơn.
