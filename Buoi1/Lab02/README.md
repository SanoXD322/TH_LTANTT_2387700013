# Lab 02 - Git hooks và kiểm tra an ninh trước khi commit

## 1. Thông tin bài làm

- Môn học: Thực hành Lập trình An ninh thông tin
- Bài: Lab 02 - Tạo Git hook tự động kiểm tra mã nguồn trước khi commit
- Mục tiêu: Ngăn chặn việc commit các file có dữ liệu nhạy cảm, file có quyền truy cập không an toàn, hoặc mã nguồn có lỗ hổng bảo mật rõ ràng.
- Công nghệ: Python, Git Hooks, Bandit

## 2. Mục tiêu của bài lab

Bài Lab 02 tập trung vào việc xây dựng cơ chế bảo vệ repository bằng Git hook, đảm bảo mọi thay đổi trước khi commit đều được quét tự động. Các kiểm tra chính gồm:

1. Phát hiện thông tin nhạy cảm như API key, secret, password, token.
2. Phát hiện file có quyền ghi công khai trên hệ thống Linux/macOS.
3. Chạy công cụ phân tích tĩnh `Bandit` để tìm các lỗ hổng Python tiềm ẩn.
4. Chặn commit nếu có bất kỳ cảnh báo nào trong các kiểm tra trên.

## 3. Cấu trúc thư mục

```text
Lab02/
|-- .githooks/
|   `-- pre-commit             # Script Git hook chính
|-- pre-commit-hook-test/
|   `-- bad.py                 # File mẫu dùng để minh họa commit bị chặn
|-- requirements.txt           # Thư viện cần cài đặt
`-- README.md                  # Báo cáo bài làm
```

## 4. Mô tả chức năng của hook

File hook được đặt tại `.githooks/pre-commit` và được thực thi trước khi `git commit` chạy. Hook hoạt động theo luồng sau:

1. Lấy danh sách các file đã được staged bằng lệnh:

```bash
git diff --cached --name-only
```

2. Duyệt từng file đã staged và kiểm tra các điều kiện sau:

- Tìm kiếm các pattern nhạy cảm như:
  - API key
  - secret
  - password
  - token
  - AWS access key
- Kiểm tra quyền file trên Unix-like system:
  - nếu file có quyền world-writable (`others write`), commit bị chặn
- Gọi Bandit để quét toàn bộ repo:

```bash
bandit -r .
```

3. Nếu phát hiện bất kỳ cảnh báo nào, hook sẽ in ra thông báo và kết thúc bằng mã lỗi `1`, làm cho commit bị từ chối.

## 5. Chi tiết kiểm tra

### 5.1. Phát hiện thông tin nhạy cảm

Hook định nghĩa các regex mẫu để phát hiện dữ liệu nhạy cảm như:

- `apikey = "..."`
- `secret = "..."`
- `password = "..."`
- `token = "..."`
- AWS access key dạng `AKIA...` hoặc `ASIA...`

Nếu phát hiện chuỗi tương ứng xuất hiện trong file đã commit, hook sẽ cảnh báo:

```text
Sensitive info found in <file>: pattern <regex>
```

### 5.2. Kiểm tra quyền file

Trên Linux/macOS, hook dùng `os.stat()` và kiểm tra cờ quyền:

```python
st.st_mode & stat.S_IWOTH
```

Nếu file đang có quyền ghi cho user khác (`others write`), hook báo lỗi và chặn commit.

### 5.3. Quét mã nguồn bằng Bandit

Bandit là công cụ quét mã Python để tìm các lỗ hổng bảo mật như:

- hardcoded password
- use of weak crypto
- unsafe subprocess
- SQL injection hoặc vulnerability patterns

Nếu Bandit phát hiện lỗi mức `High`, hook sẽ từ chối commit.

## 6. Cài đặt và kích hoạt hook

### 6.1. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 6.2. Kích hoạt hook

Có 2 cách phổ biến:

#### Cách 1: Dùng thư mục `.githooks`

```bash
git config core.hooksPath .githooks
```

#### Cách 2: Copy file hook vào `.git/hooks`

```bash
cp .githooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## 7. Mô phỏng kiểm thử

Trong thư mục `pre-commit-hook-test`, có file mẫu `bad.py` dùng để kiểm tra việc hook chặn commit. Nội dung mẫu có thể chứa các dữ liệu nhạy cảm hoặc code tiềm ẩn. Khi file này được thêm vào stage và commit, hook sẽ phát hiện và chặn hành động.

Ví dụ:

```bash
git add pre-commit-hook-test/bad.py
git commit -m "Test pre-commit hook"
```

Kết quả mong đợi:

```text
COMMIT BLOCKED by GitSecure:
 - Sensitive info found in pre-commit-hook-test/bad.py: pattern ...
```

## 8. Kết quả đạt được

Sau khi triển khai hook, repository đã có khả năng:

- ngăn commit dữ liệu bí mật trong source code;
- phát hiện file có quyền truy cập quá rộng;
- kiểm tra mã nguồn Python bằng Bandit;
- đảm bảo mọi commit đi qua một lớp kiểm tra bảo mật cơ bản trước khi lưu vào git history.

## 9. Đánh giá và hạn chế

### Ưu điểm

- Hoạt động tự động, không cần người dùng kiểm tra thủ công.
- Giảm nguy cơ rò rỉ secret hoặc token khi push lên repository.
- Phù hợp cho môi trường học tập và phát triển nhỏ.

### Hạn chế

- Regex phát hiện secret chỉ là cơ chế blacklist đơn giản, chưa đầy đủ cho mọi trường hợp.
- Bandit có thể phát hiện nhiều cảnh báo không phải lỗi nghiêm trọng trong môi trường thực tế.
- Hook này phù hợp cho môi trường học tập, chưa phải là bộ kiểm tra bảo mật doanh nghiệp hoàn chỉnh.

## 10. Kết luận

Lab 02 đã thành công trong việc xây dựng một Git hook giúp tự động kiểm tra mã nguồn trước khi commit. Đây là một bước quan trọng trong việc tăng cường an ninh cho quá trình phát triển phần mềm, đặc biệt khi làm việc với source code và repository có nhiều thành viên.

Thông qua bài tập này, tôi hiểu rõ hơn vai trò của `pre-commit` trong việc ngăn lỗi bảo mật sớm, giúp giảm thiểu rủi ro trước khi thay đổi được lưu vào lịch sử version control.
