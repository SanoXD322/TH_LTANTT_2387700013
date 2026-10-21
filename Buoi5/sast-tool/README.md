# Báo cáo bài thực hành: SAST Tool

## 1. Mục tiêu

SAST (Static Application Security Testing) là kiểm tra mã nguồn mà không cần chạy chương trình. Bài thực hành này xây dựng công cụ Python nhỏ mang tên PySAST: phân tích cú pháp bằng AST, tìm một số mẫu mã đáng chú ý, kiểm tra chất lượng mã bằng Flake8, áp dụng mức độ nghiêm trọng theo ruleset và xuất kết quả theo định dạng SARIF 2.1.0.

## 2. Luồng xử lý

Khi chạy `sast_tool.main`, công cụ thực hiện các bước:

1. Đọc nội dung tệp Python đầu vào.
2. `ASTAnalyzer` duyệt cây cú pháp để phát hiện lời gọi `eval()`.
3. `VulnPatternMatcher` tìm các mẫu regex gồm gán mật khẩu dạng chuỗi và import `pickle`.
4. `CodeQualityChecker` chạy Flake8 trên tệp và chuyển các dòng cảnh báo đọc được thành phát hiện.
5. `SecurityRuleEngine` đối chiếu loại phát hiện với `rules/default_rules.json`, gán mức độ `high`, `medium` hoặc `low` theo loại.
6. `SarifReporter` ghi các phát hiện thành tệp `report.sarif`.

Mã ví dụ có chủ đích chứa những mẫu để kiểm tra nằm trong `examples/vulnerable_01.py` và `examples/vulnerable_02.py`. Chỉ sử dụng chúng làm dữ liệu thử nghiệm trong bài thực hành.

## 3. Cài đặt

Mở terminal tại thư mục `Buoi5/sast-tool`, sau đó cài các thư viện trong `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Các gói khai báo gồm `flake8`, `sarif-om` và `jsonpickle`.

## 4. Cách chạy

Chạy từ thư mục gốc của dự án để đường dẫn ruleset mặc định `rules/default_rules.json` được tìm thấy:

```bash
python -m sast_tool.main examples/vulnerable_01.py
```

Khi phân tích xong, chương trình in số lượng phát hiện và ghi đè kết quả tại `report.sarif` trong thư mục hiện hành. Có thể thay đối số bằng đường dẫn đến tệp Python khác. Tệp đầu vào phải parse được thành cú pháp Python hợp lệ; lỗi cú pháp sẽ làm quá trình phân tích dừng.

## 5. Kết quả đầu ra

`report.sarif` chứa một SARIF log phiên bản `2.1.0`, nhận diện tool là `PySAST` phiên bản `1.0.0`. Mỗi kết quả bao gồm thông điệp và vị trí dòng/cột được phát hiện để hỗ trợ xem lại trong các công cụ có hỗ trợ SARIF.

Các mức nghiêm trọng trong ruleset mặc định:

| Loại phát hiện | Mức độ |
| --- | --- |
| `Use of eval` | Cao (`high`) |
| `Pattern Match` | Trung bình (`medium`) |
| `Lint Issue` | Thấp (`low`) |

## 6. Kiểm thử

Chạy các bài kiểm thử `unittest` từ thư mục dự án:

```bash
python -m unittest discover -s tests
```

Các test hiện có kiểm tra các phần AST, matcher, rule engine, kiểm tra chất lượng mã và xuất SARIF.

## 7. Nhận xét và giới hạn

- Phân tích AST hiện chỉ nhận diện lời gọi `eval` khi tên hàm được viết trực tiếp là `eval`; các cách gọi gián tiếp hoặc tên đã được gán lại có thể không được phát hiện.
- Regex cho mật khẩu và `pickle` là mẫu đơn giản, có thể bỏ sót cách viết khác hoặc tạo cảnh báo không chính xác. Việc tìm `pickle` hiện dựa trên mẫu văn bản `import pickle`.
- Ruleset chỉ gán severity theo chuỗi `type`; đây chưa phải bộ luật phân tích đầy đủ và chưa sử dụng mọi thuộc tính của rule để đánh giá ngữ cảnh.
- Kết quả Flake8 phụ thuộc vào cấu hình/môi trường cài đặt. Công cụ hiện chuyển đầu ra tiêu chuẩn thành phát hiện lint.
- SARIF giúp chuẩn hóa trao đổi kết quả, nhưng không đảm bảo các phát hiện đã được xác minh đúng. Cần xem lại mã nguồn và đánh giá thủ công trước khi kết luận có lỗ hổng.

## 8. Kết luận

Bài thực hành thể hiện một pipeline SAST cơ bản gồm phân tích cú pháp, khớp mẫu, áp dụng ruleset, kiểm tra lint và xuất SARIF. Đây là nền tảng minh họa có thể mở rộng bằng ruleset phong phú hơn và các phép phân tích ngữ nghĩa sâu hơn; hiện tại không nên xem kết quả là đánh giá bảo mật toàn diện.

## 9. Hình ảnh kết quả

### Ảnh 1: Kết quả chạy phân tích
![alt text](<Screenshot 2026-10-21 090104.png>)



<!-- Dán ảnh kết quả chạy công cụ và số lượng phát hiện tại đây. -->

<br><br><br><br>

### Ảnh 2: Báo cáo SARIF
![alt text](<Screenshot 2026-10-21 090203.png>)
![alt text](<Screenshot 2026-10-21 090248.png>)


<!-- Dán ảnh nội dung `report.sarif` hoặc kết quả mở báo cáo tại đây. -->

<br><br><br><br>