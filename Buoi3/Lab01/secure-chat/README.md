# Lab 01 - Ứng dụng chat an toàn bằng TLS và AES

## 1. Thông tin bài làm

- Môn học: Thực hành Lập trình An ninh thông tin
- Bài: Lab 01 - Xây dựng ứng dụng chat an toàn với chứng chỉ TLS và mã hóa AES
- Công nghệ: Python, OpenSSL, TLS/SSL, AES-256, socket
- Mục tiêu: Thiết kế một hệ thống chat đơn giản nhưng đảm bảo tính bảo mật khi truyền dữ liệu giữa client và server.

## 2. Mục tiêu bài lab

Lab 01 tập trung vào việc xây dựng một ứng dụng chat có tính bảo mật cơ bản bằng cách kết hợp:

1. Mã hóa tin nhắn bằng thuật toán AES-256.
2. Xác thực kết nối bằng chứng chỉ TLS và CA riêng.
3. Tạo kênh truyền thông tin an toàn giữa server và client.
4. Kiểm tra khả năng giao tiếp đồng thời giữa nhiều client trong môi trường máy tính cục bộ.

## 3. Tổng quan hệ thống

Hệ thống bao gồm 3 thành phần chính:

- `server.py`: lắng nghe kết nối từ client, xác thực TLS và relay tin nhắn giữa các client.
- `client.py`: khởi tạo kết nối TLS tới server, nhập username và gửi/nhận tin nhắn.
- `message_encryption.py`: thực hiện mã hóa và giải mã dữ liệu theo AES-CBC.

Ngoài ra, hệ thống còn có các module hỗ trợ:

- `connection_manager.py`: quản lý các client đang kết nối.
- `room_manager.py`: quản lý phòng chat cơ bản.
- `make-certs.bat`: tự động tạo chứng chỉ CA, server cert và client cert.
- `certs/`: lưu trữ chứng chỉ và khóa riêng của hệ thống.

## 4. Cấu trúc thư mục

```text
Buoi3/
|-- README.md                  # Báo cáo lab
|-- server.py                  # Server chat an toàn
|-- client.py                  # Client chat an toàn
|-- message_encryption.py      # AES encryption/decryption
|-- connection_manager.py      # Quản lý kết nối
|-- room_manager.py            # Quản lý phòng chat
|-- make-certs.bat             # Script tạo chứng chỉ TLS
|-- openssl.cnf                # Cấu hình OpenSSL
|-- certs/
|   |-- ca/
|   |-- server/
|   `-- client/
`-- __pycache__/              # Cache Python (nếu có)
```

## 5. Cách hoạt động

### 5.1. Tạo chứng chỉ TLS

Hệ thống sử dụng chứng chỉ tự ký để mô phỏng môi trường TLS thực tế.

Bước thực hiện:

```powershell
make-certs.bat
```

Script sẽ tạo:

- CA certificate: `certs/ca/ca.crt`
- Server certificate: `certs/server/server.crt`
- Server private key: `certs/server/server.key`
- Client certificate: `certs/client/client.crt`
- Client private key: `certs/client/client.key`

### 5.2. Khởi động server

```powershell
python server.py
```

Khi server chạy, nó sẽ mở cổng `127.0.0.1:8443` và chờ client kết nối.

### 5.3. Khởi động client

Mở một terminal mới và chạy:

```powershell
python client.py
```

Client sẽ:

- nhập `Username`
- tạo khóa AES 256-bit ngẫu nhiên
- gởi thông tin username + key tới server
- kết nối qua TLS
- bắt đầu gửi/nhận tin nhắn

## 6. Mô tả chức năng

### 6.1. Mã hóa tin nhắn

Tin nhắn được mã hóa bằng AES-CBC với khóa 256-bit.

- Mỗi tin nhắn trước khi gửi qua network đều được mã hóa.
- Server và client dùng cùng khóa để giải mã.
- Việc này giúp bảo vệ nội dung tin nhắn khi truyền trên mạng.

### 6.2. Bảo mật tầng kết nối

Server và client đều xác thực chứng chỉ bằng CA đã được cấp trước đó.

- `CERT_REQUIRED` được bật để ép client/server xác minh chứng chỉ.
- Chỉ những thiết bị có chứng chỉ hợp lệ mới được kết nối.
- Cấu hình TLS chỉ cho phép các phiên bản an toàn hơn.

### 6.3. Chuyển tiếp tin nhắn

Khi một client gửi tin nhắn:

1. client mã hóa tin nhắn;
2. gửi tới server;
3. server giải mã và nhận diện người gửi;
4. server gửi lại cho các client còn lại.

## 7. Cài đặt môi trường

### 7.1. Yêu cầu

- Python 3.9+
- OpenSSL
- Thư viện `cryptography`

### 7.2. Cài đặt thư viện cần thiết

```powershell
pip install cryptography
```

Nếu máy của bạn chưa có OpenSSL, hãy cài đặt theo hướng dẫn của hệ điều hành tương ứng.

## 8. Hướng dẫn chạy thử

### Bước 1: Tạo chứng chỉ

```powershell
cd Buoi3
make-certs.bat
```

### Bước 2: Chạy server

```powershell
python server.py
```

### Bước 3: Chạy client 1

```powershell
python client.py
```

Nhập username ví dụ:

```text
Alice
```

### Bước 4: Chạy client 2

Mở thêm 1 terminal và chạy lại:

```powershell
python client.py
```

Nhập username ví dụ:

```text
Bob
```

### Bước 5: Gửi tin nhắn

- Alice nhập: `Xin chào Bob`
- Bob nhập: `Chào Alice`
- Các tin nhắn sẽ được hiển thị trên cả 2 client nếu kết nối hoạt động đúng.

## 9. Kết quả đạt được

Sau khi triển khai, ứng dụng đã hoàn thành các tiêu chí chính sau:

- kết nối giữa client và server an toàn hơn nhờ TLS;
- tin nhắn truyền đi dưới dạng dữ liệu đã mã hóa;
- server có khả năng nhận và relay tin nhắn cho các client khác;
- hệ thống có thể mở rộng cho các phòng chat hoặc nhiều người dùng.

## 10. Ảnh minh họa / kết quả chạy

> Dán ảnh kết quả thực tế vào các vị trí dưới đây sau khi chạy demo.

### 10.1. Giao diện server đang chạy

```markdown
![Hình 1: Server đang chạy trên localhost:8443](./assets/server-running.png)
```
<img width="1035" height="162" alt="image" src="https://github.com/user-attachments/assets/92424bc8-a7d6-44ef-87e0-79bda62c0ab3" />


### 10.2. Client kết nối và gửi tin nhắn

```markdown
![Hình 2: Client đăng nhập và gửi tin nhắn](./assets/client-chat.png)
```
<img width="1017" height="250" alt="image" src="https://github.com/user-attachments/assets/7b2c51c1-883f-4abe-9391-de4ebfb95ebe" />

### 10.3. Kết quả trao đổi giữa hai client

```markdown
![Hình 3: Hai client trao đổi tin nhắn an toàn](./assets/chat-demo.png)
```
<img width="1042" height="402" alt="image" src="https://github.com/user-attachments/assets/d84ef32e-24c1-4373-a946-5e3f28275423" />

## 11. Nhận xét và bài học

Qua bài lab này, tôi đã hiểu rõ hơn về:

- cách xây dựng ứng dụng mạng cơ bản trong Python;
- cách sử dụng OpenSSL để tạo chứng chỉ và CA;
- cách áp dụng TLS để bảo vệ kết nối;
- cách triển khai AES để mã hóa dữ liệu trước khi truyền đi;
- tầm quan trọng của xác thực chứng chỉ trong môi trường an ninh mạng.

## 12. Kết luận

Lab 01 đã giúp xây dựng một ứng dụng chat có mức bảo mật cơ bản, phù hợp cho mô phỏng các hệ thống truyền tin an toàn trong môi trường học tập. Đây là nền tảng quan trọng để phát triển các hệ thống mạng có tính bảo mật cao hơn trong các bài tập sau.
