# Báo cáo bài thực hành: DAST Tool

## 1. Mục tiêu

DAST (Dynamic Application Security Testing) là cách kiểm tra ứng dụng khi chương trình đang chạy. Bài thực hành này xây dựng một bộ công cụ Python minh họa việc quan sát tiến trình và một số thông tin hệ thống trong thời gian chạy. Các thành phần được ghép trong `main.py` và có thể được gọi qua API Flask trong `app.py`.

> **Phạm vi thực tế:** phiên bản hiện tại chủ yếu theo dõi chính tiến trình của công cụ. Đây là mô hình minh họa, chưa phải bộ quét DAST hoàn chỉnh có khả năng tự kiểm thử các ứng dụng web tùy ý.

## 2. Chức năng và thành phần

| Thành phần | Chức năng hiện có |
| --- | --- |
| `RuntimeMonitor` | Dùng `psutil` lấy mức sử dụng CPU, bộ nhớ RSS và danh sách tệp đang mở của PID được truyền vào. |
| `MemoryAnalyzer` | Gọi garbage collector, đọc các đối tượng còn trong `gc.garbage` có `__del__`, và đánh dấu số nguyên có trị tuyệt đối lớn hơn `2**63` như một phép kiểm tra tràn số đơn giản. |
| `NetworkTrafficAnalyzer` | Lấy bộ đếm I/O mạng theo từng giao diện mạng qua `psutil.net_io_counters(pernic=True)`. Đây là số liệu tổng hợp theo giao diện, không phải lưu lượng được quy về tiến trình riêng. |
| `SecurityBehaviorChecker` | Tìm các chuỗi `os.system`, `eval`, `exec` trong chính tệp triển khai bộ kiểm tra. Đây chưa phải cơ chế theo dõi lời gọi hệ thống thực tế của tiến trình được kiểm tra. |
| `VirtualSandbox` | Chạy lệnh trong thư mục tạm và trả lại stdout/stderr. Thư mục làm việc riêng **không phải** cơ chế cách ly hệ điều hành. |
| Flask API | Cung cấp các endpoint để đọc số liệu monitor, memory, network, security và gửi yêu cầu chạy sandbox. |

## 3. Cài đặt

Mở terminal tại thư mục `Buoi5/dast-tool`, sau đó cài các thư viện trong `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Các thư viện được khai báo là `psutil` và `Flask`.

## 4. Cách chạy

### Chạy bản tổng hợp trên terminal

```bash
python main.py
```

Chương trình sẽ lần lượt in thông tin tiến trình hiện tại, kết quả các phép kiểm tra memory/network/security, và kết quả chạy thử trong thư mục tạm.

### Chạy API

```bash
python app.py
```

Mặc định Flask chạy cổng `5000`. Các endpoint được khai báo như sau:

| Phương thức | Đường dẫn | Nội dung |
| --- | --- | --- |
| `GET` | `/api/monitor` | CPU, RSS memory và đường dẫn các tệp đang mở |
| `GET` | `/api/memory` | Kết quả kiểm tra garbage collector và phép thử số nguyên |
| `GET` | `/api/network` | Bộ đếm I/O của các giao diện mạng |
| `GET` | `/api/security` | Các chuỗi đáng chú ý được tìm trong mã của checker |
| `POST` | `/api/sandbox` | Nhận JSON có trường `command`, trả stdout/stderr từ lệnh được chạy |

### Cảnh báo an toàn

Không đưa API này lên mạng hoặc sử dụng với dữ liệu không đáng tin cậy. Ứng dụng hiện bind vào `0.0.0.0`; endpoint sandbox chuyển lệnh nhận được cho `subprocess.run` với `shell=True`. Vì vậy, thư mục tạm **không ngăn lệnh truy cập hệ thống**, và endpoint này có thể dẫn đến thực thi lệnh trên máy chạy ứng dụng. Chỉ thử nghiệm trong môi trường cá nhân/được phép, không chứa dữ liệu quan trọng; không coi sandbox hiện tại là vùng cách ly an toàn.

## 5. Kiểm thử

Chạy các bài kiểm thử `unittest` từ thư mục dự án:

```bash
python -m unittest discover -s tests
```

Các test hiện có kiểm tra những hành vi cơ bản của bộ phân tích memory, network, runtime, security checker và sandbox.

## 6. Nhận xét và giới hạn

- Bộ công cụ minh họa được cách thu thập một số chỉ số runtime, nhưng chưa có cơ chế điều khiển ứng dụng mục tiêu, gửi payload kiểm thử web, hay tổng hợp phát hiện DAST cho một ứng dụng độc lập.
- Phép kiểm tra “memory leak” chỉ xem `gc.garbage` sau khi thu gom; nó không chứng minh được ứng dụng có hay không có rò rỉ bộ nhớ.
- Phép kiểm tra overflow chỉ áp dụng một ngưỡng số nguyên quy ước, không mô phỏng tràn số ở mọi kiểu dữ liệu hay runtime.
- Network stats là bộ đếm toàn giao diện; security checker quét văn bản của tệp checker chứ không giám sát hành vi động.
- Sandbox hiện tại chỉ đặt working directory vào thư mục tạm. Muốn dùng cho phân tích thực tế cần thay bằng cơ chế cách ly được thiết kế và cấu hình an toàn, đồng thời giới hạn lệnh đầu vào và quyền truy cập.

## 7. Kết luận

Bài thực hành kết hợp `psutil`, Python và Flask để minh họa các bước quan sát một tiến trình đang chạy. Kết quả phù hợp cho mục tiêu học tập và thử nghiệm cục bộ; các giới hạn về phạm vi phân tích và sandbox cần được khắc phục trước khi cân nhắc sử dụng trong môi trường thực tế.

## 8. Hình ảnh kết quả

### Ảnh 1: Kết quả chạy chương trình trên terminal
![alt text](<Screenshot 2026-10-21 090411.png>)
![alt text](<Screenshot 2026-10-21 090454.png>)


<!-- Dán ảnh kết quả chạy `python main.py` tại đây. -->

<br><br><br><br>

### Ảnh 2: Kết quả kiểm tra API
![alt text](<Screenshot 2026-10-21 090527.png>)


<!-- Dán ảnh kết quả gọi các endpoint API tại đây. -->

<br><br><br><br>