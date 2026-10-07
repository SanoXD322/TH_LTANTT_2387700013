# Lab 02 - NetRecon Network Reconnaissance Toolkit

## 1. Thông tin bài lab

- Môn học: Thực hành Lập trình An ninh thông tin
- Bài: Lab 02 - Xây dựng công cụ khảo sát dịch vụ mạng NetRecon
- Ngôn ngữ: Python
- Giao diện web: Flask, HTML, HTMX
- Công cụ dò dịch vụ: Nmap

## 2. Mục tiêu

NetRecon minh họa cách xây dựng một công cụ khảo sát mạng có thể chạy từ dòng lệnh hoặc giao diện web. Người dùng chọn máy đích, danh sách cổng và chế độ kiểm tra; chương trình thực hiện một hoặc nhiều tác vụ rồi hiển thị kết quả trên web và gửi kết quả qua email nếu SMTP được cấu hình.

> **Phạm vi sử dụng:** Chỉ quét các thiết bị và mạng do bạn sở hữu hoặc được cho phép kiểm tra. Việc quét hệ thống không có sự cho phép có thể vi phạm quy định hoặc pháp luật.

## 3. Chức năng

| Chế độ | Mô tả |
| --- | --- |
| `scan` | Thử kết nối TCP bất đồng bộ tới các cổng đã chọn; cổng mở được ghi ra terminal và file log. |
| `service` | Gọi Nmap với tùy chọn `-sV` để nhận diện dịch vụ trên các cổng đã chọn. |
| `banner` | Kết nối tới từng cổng và thử đọc banner dịch vụ. |
| `map` | Đọc bảng ARP của máy đang chạy chương trình bằng lệnh `arp -a`. |
| `vuln` | Đối chiếu số cổng với danh sách CVE được khai báo tĩnh trong chương trình. Đây không phải là kiểm tra xác nhận lỗ hổng trên máy đích. |
| `all` | Chạy lần lượt tất cả các chế độ trên. |

## 4. Cấu trúc thư mục

```text
Lab02/
|-- README.md
`-- netrecon/
    |-- app.py                 # Ứng dụng Flask
    |-- cli.py                 # Giao diện dòng lệnh
    |-- requirements.txt       # Các gói Python
    |-- modules/
    |   |-- port_scanner.py    # Quét cổng TCP bất đồng bộ
    |   |-- service_detector.py# Nhận diện dịch vụ qua Nmap
    |   |-- banner_grabber.py  # Thu thập banner
    |   |-- network_mapper.py  # Đọc bảng ARP
    |   |-- vuln_checker.py    # Đối chiếu cổng với danh sách CVE
    |   `-- email_sender.py    # Gửi kết quả qua email
    |-- templates/             # Các trang HTML của Flask
    `-- static/                # CSS của giao diện
```

## 5. Yêu cầu

- Windows, Linux hoặc macOS
- Python 3.9 trở lên
- Nmap nếu sử dụng chế độ `service` hoặc `all`
- Kết nối mạng và thông tin SMTP hợp lệ nếu muốn gửi kết quả qua email

## 6. Cài đặt

Mở terminal tại thư mục dự án:

```powershell
cd Buoi3\Lab02\netrecon
```

Tạo và kích hoạt môi trường ảo trên Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Cài các thư viện được khai báo:

```powershell
python -m pip install -r requirements.txt
```

Cài Nmap riêng theo hệ điều hành nếu chưa có, sau đó kiểm tra Nmap có thể được gọi từ terminal:

```powershell
nmap --version
```

## 7. Cấu hình email (không bắt buộc)

Ứng dụng đọc hai biến môi trường `SMTP_USER` và `SMTP_PASS` để đăng nhập SMTP Gmail. Có thể khai báo trong file `.env` ở thư mục `netrecon`:

```dotenv
SMTP_USER=your-email@example.com
SMTP_PASS=your-app-password
```

Thay giá trị mẫu bằng thông tin phù hợp với tài khoản của bạn. Với Gmail, thường cần dùng App Password thay vì mật khẩu đăng nhập thông thường. Không đưa thông tin thật vào README, ảnh chụp, hoặc Git.

## 8. Chạy ứng dụng web

Từ thư mục `netrecon`, chạy:

```powershell
python app.py
```

Mở trình duyệt tại [http://127.0.0.1:5000](http://127.0.0.1:5000). Nhập địa chỉ IP/hostname đích, danh sách cổng cách nhau bằng dấu phẩy, chọn chế độ, nhập email nhận kết quả rồi nhấn **Scan**.

Ví dụ danh sách cổng:

```text
22,80,443
```

## 9. Chạy giao diện dòng lệnh

Ví dụ quét các cổng 22, 80 và 443 trên máy đích được phép kiểm tra:

```powershell
python cli.py --target 192.168.1.10 --ports 22,80,443 --mode all
```

Chỉ chạy một chế độ bằng cách thay `all` bằng `scan`, `service`, `banner`, `map` hoặc `vuln`. Có thể dùng `--rate-limit` để thay đổi số kết nối quét đồng thời:

```powershell
python cli.py --target 192.168.1.10 --ports 22,80,443 --mode scan --rate-limit 50
```

## 10. Lưu ý khi xem kết quả

- Chế độ quét cổng hiện ghi các cổng mở ra terminal của tiến trình Flask/CLI và file `netrecon.log`. Hàm quét hiện chưa trả danh sách cổng cho trang web hiển thị.
- Chế độ nhận diện dịch vụ yêu cầu Nmap đã cài đặt và có thể gọi từ `PATH`.
- Bảng ARP là thông tin từ máy đang chạy NetRecon, không phải sơ đồ đầy đủ của mạng.
- Chế độ `vuln` chỉ đối chiếu số cổng với danh sách CVE viết sẵn; kết quả không chứng minh máy đích thực sự có lỗ hổng.
- Gửi email phụ thuộc vào cấu hình SMTP. Nếu email không gửi được, hãy kiểm tra thông báo ở terminal và cấu hình tài khoản.

## 11. Ảnh minh họa và kết quả

Tạo thư mục `images` cùng cấp với README này rồi lưu ảnh chụp vào đó theo tên bên dưới, hoặc sửa đường dẫn ảnh cho khớp với tên file của bạn.

### 11.1. Giao diện nhập thông tin quét

<!-- Chèn ảnh giao diện web tại images/01-web-form.png -->
![Hình 1: Giao diện nhập thông tin quét]
<img width="1392" height="565" alt="image" src="https://github.com/user-attachments/assets/abc15b6c-cf9d-4dc8-8322-70a757a98a5d" />

### 11.2. Kết quả hiển thị trên trang web

<!-- Chèn ảnh kết quả trên trình duyệt tại images/02-web-result.png -->
![Hình 2: Kết quả khảo sát hiển thị trên web]
<img width="916" height="927" alt="Screenshot 2026-10-07 095037" src="https://github.com/user-attachments/assets/05e0a184-1992-4bbf-be28-c9b8bad46a64" />

### 11.3. Kết quả chạy từ terminal

<!-- Chèn ảnh terminal chạy NetRecon tại images/03-terminal-result.png -->
![Hình 3: Kết quả chạy NetRecon từ terminal](./images/03-terminal-result.png)
<img width="635" height="151" alt="image" src="https://github.com/user-attachments/assets/f2e57907-297c-449d-95b1-17bd3777876c" />

### 11.4. Kết quả email (nếu đã cấu hình SMTP)

<!-- Chèn ảnh email nhận được tại images/04-email-result.png -->
![Hình 4: Email kết quả NetRecon](./images/04-email-result.png)
<img width="977" height="742" alt="image" src="https://github.com/user-attachments/assets/88c57b1a-6396-4d62-a41f-da7a46cd2f10" />

## 12. Kết luận

Qua bài lab, người thực hiện làm quen với việc tổ chức một ứng dụng Python thành các module, xây dựng giao diện web bằng Flask, xử lý tác vụ mạng cơ bản và gọi công cụ Nmap. NetRecon phù hợp cho mục đích học tập, thử nghiệm trong môi trường được cho phép; các kết quả cần được xác minh bằng công cụ và quy trình kiểm tra phù hợp trước khi đưa ra kết luận về bảo mật.
