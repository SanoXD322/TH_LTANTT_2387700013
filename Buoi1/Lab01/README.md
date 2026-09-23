# Lab 01 - SecureValidator

## 1. Thông tin bài làm

- **Môn học:** Thực hành Lập trình An ninh thông tin
- **Bài:** Lab 01 - Xây dựng các hàm kiểm tra và xử lý dữ liệu đầu vào an toàn
- **Ứng dụng:** SecureValidator
- **Công nghệ:** Python, Flask, HTML/Jinja2, unittest

## 2. Mục tiêu

Lab 01 xây dựng một ứng dụng web đơn giản cho phép người dùng nhập dữ liệu và kiểm tra các trường hợp đầu vào phổ biến trong an ninh ứng dụng web. Bài làm tập trung vào:

1. Kiểm tra định dạng email.
2. Kiểm tra URL chỉ sử dụng giao thức HTTP/HTTPS.
3. Ngăn chặn path traversal thông qua tên file.
4. Lọc một số ký tự và từ khóa nguy hiểm trong chuỗi SQL.
5. Mã hóa HTML để giảm nguy cơ Cross-Site Scripting (XSS).
6. Viết unit test cho các trường hợp hợp lệ, không hợp lệ và payload tấn công mẫu.

## 3. Cấu trúc thư mục

```text
Lab01/
|-- app.py                         # Ứng dụng Flask và route xử lý form
|-- requirements.txt               # Danh sách thư viện Python
|-- securevalidator/
|   |-- __init__.py                # Export các hàm validator
|   `-- core.py                    # Các hàm kiểm tra và làm sạch dữ liệu
|-- templates/
|   `-- index.html                 # Giao diện nhập liệu và hiển thị kết quả
`-- tests/
    `-- test_validators.py         # Unit test cho các hàm xử lý
```

## 4. Mô tả chức năng

### 4.1. Kiểm tra email

Hàm `validate_email()` sử dụng biểu thức chính quy để kiểm tra email có dạng cơ bản:

```text
<tên>@<miền>.<đuôi>
```

Ví dụ:

- `user@example.com` được chấp nhận.
- `user@@example..com` bị từ chối.

Hàm trả về `True` nếu email hợp lệ theo mẫu và `False` nếu không khớp. Đây là kiểm tra định dạng cơ bản, không xác nhận email có tồn tại thật hay có thể nhận thư.

### 4.2. Kiểm tra URL

Hàm `validate_url()` phân tích URL bằng `urllib.parse.urlparse()` và chỉ chấp nhận:

- Scheme là `http` hoặc `https`.
- URL có `netloc`.

Ví dụ:

- `https://example.com` được chấp nhận.
- `ftp://example.com` bị từ chối.

Mục đích của hàm là loại bỏ các URL sai giao thức ở mức cơ bản. Đây không phải là cơ chế SSRF đầy đủ; nếu ứng dụng thực hiện request tới URL đó, cần bổ sung kiểm tra DNS, địa chỉ IP nội bộ, redirect và danh sách cho phép domain.

### 4.3. Kiểm tra tên file và path traversal

Hàm `validate_filename()` ngăn chặn các dấu hiệu path traversal bằng cách từ chối:

- Chuỗi `..`.
- Dấu `/`.
- Dấu `\\`.
- Tên không trùng với kết quả của `os.path.basename()`.

Ví dụ:

- `report.pdf` được chấp nhận.
- `../../etc/passwd` bị từ chối.

Hàm phù hợp để kiểm tra tên file đơn giản. Khi xử lý upload file trong hệ thống thật, vẫn cần thêm giới hạn phần mở rộng, kích thước, nội dung file và lưu file vào thư mục an toàn.

### 4.4. Làm sạch đầu vào SQL

Hàm `sanitize_sql_input()` thực hiện hai bước:

1. Loại bỏ một số ký tự đặc biệt: `--`, `;`, dấu nháy đơn, dấu nháy kép và `#`.
2. Loại bỏ một số từ khóa SQL phổ biến: `OR`, `AND`, `SELECT`, `INSERT`, `DELETE`, `UPDATE`, `DROP`, `UNION`, `WHERE`.

Ví dụ payload kiểm thử:

```text
'' OR 1=1 --
```

Sau khi xử lý, các thành phần nguy hiểm mẫu sẽ bị loại bỏ.

> **Lưu ý bảo mật:** Cách lọc theo blacklist chỉ mang tính minh họa cho bài lab và không thay thế prepared statement. Trong ứng dụng thực tế, phải dùng parameterized query/ORM và không nối chuỗi SQL trực tiếp từ đầu vào người dùng.

### 4.5. Mã hóa đầu vào HTML

Hàm `sanitize_html_input()` sử dụng `html.escape()` để chuyển các ký tự HTML đặc biệt thành entity an toàn.

Ví dụ:

```html
<script>alert('XSS')</script>
```

được chuyển thành:

```text
&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;
```

Cách này ngăn trình duyệt diễn giải chuỗi đầu vào như một thẻ HTML/script khi chuỗi được hiển thị trên giao diện.

## 5. Luồng xử lý ứng dụng

1. Người dùng truy cập route `/` bằng phương thức `GET`.
2. Flask hiển thị form trong `templates/index.html`.
3. Khi submit form bằng `POST`, ứng dụng đọc 5 trường:
   - `email`
   - `url`
   - `filename`
   - `sql`
   - `html`
4. Dữ liệu được chuyển qua các hàm trong package `securevalidator`.
5. Kết quả validation và giá trị đã xử lý được truyền lại template.
6. Giao diện hiển thị trạng thái hợp lệ/không hợp lệ, chuỗi SQL đã lọc và chuỗi HTML đã escape.

## 6. Giao diện

Giao diện được viết bằng HTML/Jinja2 và sử dụng Pico.css từ CDN. Form gồm 5 trường đầu vào và hiển thị kết quả ngay trên cùng trang sau khi submit.

- Màu xanh: dữ liệu hợp lệ.
- Màu đỏ: dữ liệu không hợp lệ.
- SQL: hiển thị chuỗi sau khi lọc.
- HTML: hiển thị chuỗi sau khi mã hóa.

Template sử dụng `{{ ... }}` của Jinja2 để render kết quả. Các giá trị trong template được Jinja2 auto-escape khi hiển thị trong HTML.

## 7. Kiểm thử

File `tests/test_validators.py` sử dụng `unittest` và bao gồm các nhóm test sau:

| Nhóm | Nội dung |
|---|---|
| Email | Email hợp lệ và email sai định dạng |
| URL | URL HTTP/HTTPS hợp lệ và URL FTP không hợp lệ |
| Filename | Tên file hợp lệ và payload path traversal |
| SQL | Payload SQL injection mẫu và văn bản thông thường |
| HTML | Payload XSS mẫu và văn bản thông thường |

Tổng cộng có 10 test case, bao gồm cả trường hợp dữ liệu an toàn và dữ liệu có dấu hiệu tấn công.

## 8. Cài đặt và chạy ứng dụng

### 8.1. Tạo môi trường ảo

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

### 8.2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 8.3. Chạy ứng dụng

```bash
python app.py
```

Sau đó mở trình duyệt tại:

```text
http://127.0.0.1:5000
```

Ứng dụng đang bật `debug=True` để phục vụ học tập và phát triển. Không nên bật debug khi triển khai công khai.

### 8.4. Chạy unit test

Từ thư mục `Lab01`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Hoặc:

```bash
python -m unittest tests.test_validators -v
```

## 9. Đánh giá bảo mật

### Đã thực hiện

- Kiểm tra định dạng email bằng regex.
- Giới hạn URL về HTTP/HTTPS.
- Chặn một số mẫu path traversal trong tên file.
- Loại bỏ một số ký tự và từ khóa SQL nguy hiểm mẫu.
- Escape HTML để phòng chống XSS khi hiển thị đầu vào.
- Có unit test cho các trường hợp tấn công cơ bản.

### Giới hạn và hướng phát triển

- Validator email chưa bao phủ toàn bộ RFC và không xác minh email tồn tại.
- Kiểm tra URL chưa phải cơ chế chống SSRF đầy đủ.
- Lọc SQL bằng blacklist không đủ an toàn cho hệ thống thực tế; cần dùng parameterized query.
- Nên bổ sung CSRF protection cho form.
- Nên thêm giới hạn độ dài và kiểm tra trường bị thiếu trong request.
- Nên tắt `debug=True` khi deploy.
- Nên bổ sung Content Security Policy, HTTPS và cookie security flags khi triển khai.
- Nên bổ sung test boundary, Unicode, input rỗng và input rất dài.

## 10. Kết luận

Lab 01 đã xây dựng được một ứng dụng Flask nhỏ để minh họa các kỹ thuật validation và sanitization đầu vào. Các hàm được tách riêng trong package `securevalidator`, có giao diện để thao tác và có unit test cho các trường hợp cơ bản. Qua bài làm, có thể thấy rằng validation và escaping là lớp bảo vệ đầu vào quan trọng, nhưng trong ứng dụng thực tế cần kết hợp thêm prepared statement, CSRF protection, kiểm soát SSRF và các biện pháp hardening khi triển khai.
