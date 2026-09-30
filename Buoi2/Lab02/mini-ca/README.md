# BÁO CÁO THỰC HÀNH: XÂY DỰNG MINI CA

## 1. Giới thiệu

Bài thực hành xây dựng một hệ thống PKI thu nhỏ (Public Key Infrastructure) bằng Python. Chương trình minh họa quy trình tạo CA gốc, CA trung gian, phát hành chứng chỉ người dùng, xác minh chuỗi chứng chỉ và thu hồi chứng chỉ bằng CRL.

## 2. Mục tiêu

- Tìm hiểu vai trò của Root CA, Intermediate CA và chứng chỉ người dùng cuối.
- Thực hành tạo cặp khóa RSA và chứng chỉ X.509.
- Minh họa việc ký, xác minh chữ ký và xây dựng chuỗi tin cậy.
- Tạo Certificate Revocation List (CRL) và kiểm tra chứng chỉ đã bị thu hồi hay chưa.
- Làm quen với ứng dụng Python có giao diện dòng lệnh và giao diện đồ họa.

## 3. Công nghệ và thuật toán

- **Ngôn ngữ:** Python.
- **Thư viện:** `cryptography` để thao tác với khóa, chứng chỉ X.509 và CRL; `tkinter` để tạo giao diện đồ họa.
- **Thuật toán khóa:** RSA 2048 bit, số mũ công khai 65537.
- **Thuật toán băm và ký:** SHA-256; chữ ký RSA được xác minh với PKCS#1 v1.5.
- **Định dạng lưu trữ:** PEM.

## 4. Thiết kế và chức năng

### 4.1. Cấp phát chứng chỉ

Hệ thống có cấu trúc phân cấp:

```text
Root CA
└── Intermediate CA
	└── User / End-Entity Certificate
```

Root CA tự ký chứng chỉ của mình và có thời hạn 10 năm. Root CA ký chứng chỉ Intermediate CA có thời hạn 5 năm. Intermediate CA ký chứng chỉ người dùng cuối có thời hạn 1 năm. Chứng chỉ CA được đánh dấu `CA=true`; chứng chỉ người dùng được đánh dấu `CA=false`.

Các hàm tạo khóa và chứng chỉ, lưu/tải tệp PEM nằm trong `ca_utils.py`. Thông tin người dùng mẫu gồm quốc gia `VN`, tổ chức `PHUOCNTMH Company` và tên chung `Phuoc_Nguyen`.

### 4.2. Xác minh chuỗi chứng chỉ

Chương trình xác minh chữ ký của chứng chỉ người dùng bằng khóa công khai của Intermediate CA, sau đó xác minh chứng chỉ Intermediate CA bằng khóa công khai của Root CA.

>Phần xác minh hiện tập trung vào chữ ký trong chuỗi; chưa kiểm tra đầy đủ thời hạn chứng chỉ, chính sách CA, mục đích sử dụng, trạng thái thu hồi hoặc độ tin cậy của Root CA theo một kho tin cậy bên ngoài.

### 4.3. Thu hồi và kiểm tra trạng thái

`revoke_utils.py` tạo hoặc cập nhật CRL do Intermediate CA ký. Khi thu hồi, số sê-ri chứng chỉ được thêm vào danh sách cùng thời điểm thu hồi và lý do mặc định `key_compromise`. CRL có thời hạn cập nhật tiếp theo là 7 ngày.

Chức năng được đặt tên “kiểm tra OCSP” trong giao diện chỉ tra số sê-ri chứng chỉ trong tệp CRL cục bộ `certs/ca_crl.pem`. Đây **không phải** triển khai giao thức OCSP và không gửi yêu cầu tới OCSP responder.

### 4.4. Giao diện

- `demo.py`: chạy lần lượt toàn bộ quy trình mẫu trong terminal.
- `demo_ui.py`: giao diện Tkinter với các thao tác tạo CA, phát hành chứng chỉ, xác minh chuỗi, thu hồi và kiểm tra trạng thái.

## 5. Cấu trúc thư mục

```text
mini-ca/
├── ca_utils.py       # Tạo khóa, tạo/cấp chứng chỉ, xác minh chuỗi
├── revoke_utils.py   # Tạo CRL, thu hồi và tra cứu trạng thái
├── demo.py           # Kịch bản chạy mẫu trên terminal
├── demo_ui.py        # Giao diện đồ họa Tkinter
├── README.md         # Báo cáo và hướng dẫn sử dụng
└── certs/            # Khóa, chứng chỉ và CRL được tạo khi chạy
```

Các tệp được tạo trong `certs/` gồm khóa/chứng chỉ Root CA, khóa/chứng chỉ Intermediate CA, khóa/chứng chỉ người dùng và CRL khi có thao tác thu hồi. Chương trình tự tạo thư mục `certs/` nếu chưa tồn tại.

## 6. Cài đặt và chạy chương trình

Mở terminal tại thư mục `mini-ca`, sau đó cài thư viện:

```bash
pip install cryptography
```

Chạy quy trình mẫu trên terminal:

```bash
python demo.py
```

Chạy giao diện đồ họa:

```bash
python demo_ui.py
```

Trong giao diện đồ họa, thực hiện theo thứ tự: tạo Root và Intermediate CA, phát hành chứng chỉ người dùng, kiểm tra chuỗi, thu hồi chứng chỉ, rồi kiểm tra trạng thái. Nên chạy lệnh từ thư mục `mini-ca` vì chương trình sử dụng đường dẫn tương đối.

## 7. Kết quả thực nghiệm

> **Ghi chú:** Các vị trí dưới đây được chừa để bổ sung ảnh chụp màn hình kết quả chạy thực tế. Hãy thay dòng hướng dẫn bằng ảnh tương ứng sau khi chạy chương trình.

### 7.1. Giao diện chương trình

Ảnh giao diện Mini CA sau khi chạy `python demo_ui.py`.

<!-- Chèn ảnh giao diện chương trình tại đây -->

### 7.2. Tạo Root CA và Intermediate CA

Ảnh thông báo tạo thành công hai CA hoặc ảnh các tệp chứng chỉ/khóa được sinh trong thư mục `certs/`.

<!-- Chèn ảnh kết quả tạo CA tại đây -->

### 7.3. Phát hành chứng chỉ người dùng

Ảnh thông báo phát hành thành công hoặc ảnh tệp `Phuoc_Nguyen_cert.pem` được tạo.

<!-- Chèn ảnh kết quả phát hành chứng chỉ tại đây -->

### 7.4. Xác minh chuỗi chứng chỉ

Ảnh kết quả xác minh chuỗi chứng chỉ. Với dữ liệu mẫu chưa bị thay đổi, kết quả dự kiến là `Chuỗi hợp lệ: True`.

<!-- Chèn ảnh kết quả xác minh chuỗi tại đây -->

### 7.5. Thu hồi chứng chỉ và kiểm tra trạng thái

Ảnh kết quả thu hồi và tra cứu trạng thái sau khi thu hồi. Kết quả tra cứu dự kiến là `Revoked` (hoặc `Đã thu hồi` trên giao diện).

<!-- Chèn ảnh kết quả thu hồi và kiểm tra trạng thái tại đây -->

## 8. Kết luận và hướng phát triển

Bài thực hành đã minh họa các thành phần cơ bản của một CA: tạo và ký chứng chỉ theo mô hình phân cấp, xác minh chữ ký, lập CRL và tra cứu trạng thái thu hồi. Hệ thống phù hợp cho mục đích học tập, chưa phải PKI hoàn chỉnh để sử dụng trong môi trường thực tế.

Có thể phát triển thêm kiểm tra thời hạn và extension của chứng chỉ, xác minh đầy đủ chính sách chuỗi tin cậy, bảo vệ khóa riêng bằng mật khẩu hoặc thiết bị lưu khóa, ngăn thêm chứng chỉ trùng vào CRL và triển khai OCSP responder đúng giao thức.

**Lưu ý bảo mật:** Khóa riêng hiện được lưu ở dạng PEM không mã hóa trong thư mục `certs/`. Cách lưu này chỉ phục vụ minh họa, không phù hợp để bảo vệ khóa trong môi trường thực tế.
