# JWT Security Tools

Dự án cung cấp một bộ công cụ kiểm tra và quản lý bảo mật JSON Web Token (JWT). Bao gồm API Gateway tích hợp xác thực, công cụ Brute-force khóa bí mật (Cracker), kiểm tra tính hợp lệ của token và mô phỏng luồng OAuth 2.0.

## Tính năng chính
*   **API Gateway:** Cổng API bảo vệ tài nguyên, yêu cầu xác thực JWT qua header.
*   **Token Manager:** Quản lý vòng đời phát hành Access Token và Refresh Token.
*   **JWT Validator:** Kiểm tra chữ ký, thời hạn và tính hợp lệ của token.
*   **JWT Cracker:** Tấn công Brute-force đa luồng để dò tìm Secret Key yếu.
*   **OAuth Client:** Mô phỏng luồng cấp phép Authorization Code Flow.

## Cài đặt

1. Cài đặt các thư viện yêu cầu:
   ```bash
   pip install -r requirements.txt
   ```

## Hướng dẫn sử dụng

### 1. Chạy kiểm thử tự động (Pytest)
Xác minh chức năng của các module:
```bash
pytest tests/
```
*Kết quả Pytest:*
<!-- CHÈN ẢNH KẾT QUẢ PYTEST VÀO BÊN DƯỚI -->
![Kết quả Pytest](link_anh_pytest_cua_ban_tai_day.png)

### 2. Khởi chạy Server và Cấp Token
Khởi chạy máy chủ API Gateway và sinh ra Access/Refresh Token:
```bash
python main.py
```
*Giao diện cấp Token:*
<!-- CHÈN ẢNH TERMINAL IN RA ACCESS TOKEN VÀO BÊN DƯỚI -->
![Token Generate](link_anh_terminal_token_cua_ban_tai_day.png)

### 3. Kiểm tra Xác thực API (cURL)
Mở một terminal khác và sử dụng Access Token vừa được cấp để truy cập tài nguyên bảo mật:
```bash
curl.exe -H "Authorization: Bearer <dán_access_token_vào_đây>" http://127.0.0.1:5000/protected
```
*Kết quả Xác thực Thành công:*
<!-- CHÈN ẢNH KẾT QUẢ CURL TRẢ VỀ "Access granted" VÀO BÊN DƯỚI -->
![Xác thực API](link_anh_curl_success_cua_ban_tai_day.png)