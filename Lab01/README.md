# Lab 01 - SecureValidator

## 1. Thong tin bai lam

- **Mon hoc:** Thuc hanh Lap trinh An ninh thong tin
- **Bai:** Lab 01 - Xay dung cac ham kiem tra va xu ly du lieu dau vao an toan
- **Ung dung:** SecureValidator
- **Cong nghe:** Python, Flask, HTML/Jinja2, unittest

## 2. Muc tieu

Lab 01 xay dung mot ung dung web don gian cho phep nguoi dung nhap du lieu va kiem tra cac truong hop dau vao pho bien trong an ninh ung dung web. Bai lam tap trung vao:

1. Kiem tra dinh dang email.
2. Kiem tra URL chi su dung giao thuc HTTP/HTTPS.
3. Ngan chan path traversal thong qua ten file.
4. Loc mot so ky tu va tu khoa nguy hiem trong chuoi SQL.
5. Ma hoa HTML de giam nguy co Cross-Site Scripting (XSS).
6. Viet unit test cho cac truong hop hop le, khong hop le va payload tan cong mau.

## 3. Cau truc thu muc

```text
Lab01/
|-- app.py                         # Ung dung Flask va route xu ly form
|-- requirements.txt               # Danh sach thu vien Python
|-- securevalidator/
|   |-- __init__.py                # Export cac ham validator
|   `-- core.py                    # Cac ham kiem tra va lam sach du lieu
|-- templates/
|   `-- index.html                 # Giao dien nhap lieu va hien thi ket qua
`-- tests/
    `-- test_validators.py         # Unit test cho cac ham xu ly
```

## 4. Mo ta chuc nang

### 4.1. Kiem tra email

Ham `validate_email()` su dung bieu thuc chinh quy de kiem tra email co dang co ban:

```text
<ten>@<mien>.<duoi>
```

Vi du:

- `user@example.com` duoc chap nhan.
- `user@@example..com` bi tu choi.

Ham tra ve `True` neu email hop le theo mau va `False` neu khong khop. Day la kiem tra dinh dang co ban, khong xac nhan email co ton tai that hay co the nhan thu.

### 4.2. Kiem tra URL

Ham `validate_url()` phan tich URL bang `urllib.parse.urlparse()` va chi chap nhan:

- Scheme la `http` hoac `https`.
- URL co `netloc`.

Vi du:

- `https://example.com` duoc chap nhan.
- `ftp://example.com` bi tu choi.

Muc dich cua ham la loai bo cac URL sai giao thuc o muc co ban. Day khong phai la co che SSRF day du; neu ung dung thuc hien request toi URL do, can bo sung kiem tra DNS, dia chi IP noi bo, redirect va danh sach cho phep domain.

### 4.3. Kiem tra ten file va path traversal

Ham `validate_filename()` ngan chan cac dau hieu path traversal bang cach tu choi:

- Chuoi `..`.
- Dau `/`.
- Dau `\\`.
- Ten khong trung voi ket qua cua `os.path.basename()`.

Vi du:

- `report.pdf` duoc chap nhan.
- `../../etc/passwd` bi tu choi.

Ham phu hop de kiem tra ten file don gian. Khi xu ly upload file trong he thong that, van can them gioi han phan mo rong, kich thuoc, noi dung file va luu file vao thu muc an toan.

### 4.4. Lam sach dau vao SQL

Ham `sanitize_sql_input()` thuc hien hai buoc:

1. Loai bo mot so ky tu dac biet: `--`, `;`, dau nhay don, dau nhay kep va `#`.
2. Loai bo mot so tu khoa SQL pho bien: `OR`, `AND`, `SELECT`, `INSERT`, `DELETE`, `UPDATE`, `DROP`, `UNION`, `WHERE`.

Vi du payload kiem thu:

```text
'' OR 1=1 --
```

Sau khi xu ly, cac thanh phan nguy hiem mau se bi loai bo.

> **Luu y bao mat:** Cach loc theo blacklist chi mang tinh minh hoa cho bai lab va khong thay the prepared statement. Trong ung dung thuc te, phai dung parameterized query/ORM va khong noi chuoi SQL truc tiep tu dau vao nguoi dung.

### 4.5. Ma hoa dau vao HTML

Ham `sanitize_html_input()` su dung `html.escape()` de chuyen cac ky tu HTML dac biet thanh entity an toan.

Vi du:

```html
<script>alert('XSS')</script>
```

duoc chuyen thanh:

```text
&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;
```

Cach nay ngan trinh duyet dien giai chuoi dau vao nhu mot the HTML/script khi chuoi duoc hien thi tren giao dien.

## 5. Luong xu ly ung dung

1. Nguoi dung truy cap route `/` bang phuong thuc `GET`.
2. Flask hien thi form trong `templates/index.html`.
3. Khi submit form bang `POST`, ung dung doc 5 truong:
   - `email`
   - `url`
   - `filename`
   - `sql`
   - `html`
4. Du lieu duoc chuyen qua cac ham trong package `securevalidator`.
5. Ket qua validation va gia tri da xu ly duoc truyen lai template.
6. Giao dien hien thi trang thai hop le/khong hop le, chuoi SQL da loc va chuoi HTML da escape.

## 6. Giao dien

Giao dien duoc viet bang HTML/Jinja2 va su dung Pico.css tu CDN. Form gom 5 truong dau vao va hien thi ket qua ngay tren cung trang sau khi submit.

- Mau xanh: du lieu hop le.
- Mau do: du lieu khong hop le.
- SQL: hien thi chuoi sau khi loc.
- HTML: hien thi chuoi sau khi ma hoa.

Template su dung `{{ ... }}` cua Jinja2 de render ket qua. Cac gia tri trong template duoc Jinja2 auto-escape khi hien thi trong HTML.

## 7. Kiem thu

File `tests/test_validators.py` su dung `unittest` va bao gom cac nhom test sau:

| Nhom | Noi dung |
|---|---|
| Email | Email hop le va email sai dinh dang |
| URL | URL HTTP/HTTPS hop le va URL FTP khong hop le |
| Filename | Ten file hop le va payload path traversal |
| SQL | Payload SQL injection mau va van ban thong thuong |
| HTML | Payload XSS mau va van ban thong thuong |

Tong cong co 10 test case, bao gom ca truong hop du lieu an toan va du lieu co dau hieu tan cong.

## 8. Cai dat va chay ung dung

### 8.1. Tao moi truong ao

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

### 8.2. Cai dat thu vien

```bash
pip install -r requirements.txt
```

### 8.3. Chay ung dung

```bash
python app.py
```

Sau do mo trinh duyet tai:

```text
http://127.0.0.1:5000
```

Ung dung dang bat `debug=True` de phuc vu hoc tap va phat trien. Khong nen bat debug khi trien khai cong khai.

### 8.4. Chay unit test

Tu thu muc `Lab01`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Hoac:

```bash
python -m unittest tests.test_validators -v
```

## 9. Danh gia bao mat

### Da thuc hien

- Kiem tra dinh dang email bang regex.
- Gioi han URL ve HTTP/HTTPS.
- Chan mot so mau path traversal trong ten file.
- Loai bo mot so ky tu va tu khoa SQL nguy hiem mau.
- Escape HTML de phong chong XSS khi hien thi dau vao.
- Co unit test cho cac truong hop tan cong co ban.

### Gioi han va huong phat trien

- Validator email chua bao phu toan bo RFC va khong xac minh email ton tai.
- Kiem tra URL chua phai co che chong SSRF day du.
- Loc SQL bang blacklist khong du an toan cho he thong thuc te; can dung parameterized query.
- Nen bo sung CSRF protection cho form.
- Nen them gioi han do dai va kiem tra truong bi thieu trong request.
- Nen tat `debug=True` khi deploy.
- Nen bo sung Content Security Policy, HTTPS va cookie security flags khi trien khai.
- Nen bo sung test boundary, Unicode, input rong va input rat dai.

## 10. Ket luan

Lab 01 da xay dung duoc mot ung dung Flask nho de minh hoa cac ky thuat validation va sanitization dau vao. Cac ham duoc tach rieng trong package `securevalidator`, co giao dien de thao tac va co unit test cho cac truong hop co ban. Qua bai lam, co the thay rang validation va escaping la lop bao ve dau vao quan trong, nhung trong ung dung thuc te can ket hop them prepared statement, CSRF protection, kiem soat SSRF va cac bien phap hardening khi trien khai.
