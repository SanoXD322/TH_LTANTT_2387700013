# Báo cáo Lab 06: Xây dựng CI/CD Pipeline với GitLab

| | |
|---|---|
| **Sinh viên** | Hoàng Xuân Đạt |
| **MSSV** | 2387700013 |
| **Tài khoản GitLab** | `SanoXD322` |
| **Ngày thực hiện** | 28/10/2026 |
| **Trang web đã deploy** | https://sanoxd322.gitlab.io/my-pipeline-tutorial-project/ |

---

## 1. Mục tiêu

- Tạo và chạy một pipeline CI/CD cơ bản trên GitLab với nhiều stage (build, test, deploy).
- Xây dựng pipeline thực tế: build một trang tài liệu tĩnh bằng **Docusaurus** và tự động deploy lên **GitLab Pages**.
- Hiểu các khái niệm: stage, job, runner, artifact, environment.

## 2. Môi trường thực hiện

| Thành phần | Phiên bản / Ghi chú |
|---|---|
| Hệ điều hành | Windows 11 |
| GitLab | GitLab.com (gói Free) |
| GitLab Runner | 19.5.1, chạy trong Docker trên máy cá nhân (executor `docker`) |
| Docker Desktop | 4.97.0 (WSL 2) |
| Node.js (trong CI) | image `node:lts` |
| Docusaurus | template `classic` |

### Về runner

Runner dùng chung (instance runner) của GitLab.com yêu cầu xác minh tài khoản bằng số điện thoại hoặc thẻ, nên pipeline đầu tiên bị **Failed**. Em đã chuyển sang dùng **project runner tự quản lý (self-managed)** chạy trên máy cá nhân:

1. Bật tính năng Virtual Machine Platform bằng `wsl --install` (quyền Administrator), rồi cài Docker Desktop.
2. Trong **Settings → CI/CD → Runners**: tắt instance runners, tạo **project runner** với tùy chọn *Run untagged jobs*.
3. Khởi động và đăng ký runner:

```powershell
docker run -d --name gitlab-runner --restart always `
  -v /var/run/docker.sock:/var/run/docker.sock `
  -v gitlab-runner-config:/etc/gitlab-runner `
  gitlab/gitlab-runner:latest

docker exec -it gitlab-runner gitlab-runner register `
  --url https://gitlab.com --token <runner-token>
# executor: docker, default image: alpine:latest
```

4. Runner được gán (assign) cho cả hai project của bài lab và hiển thị trạng thái **Online**.

![Runner tự quản lý ở trạng thái Online]
<img width="945" height="655" alt="Screenshot 2026-10-28 093824" src="https://github.com/user-attachments/assets/f36af615-28e4-4eba-b4cd-7a9df1d8cc6d" />

---

## 3. Phần 1 (6.2.1): Pipeline đơn giản

**Project:** `hoangdat-group/hoangdat-project`

### File `.gitlab-ci.yml`

```yaml
build-job:
  stage: build
  script:
    - echo "Hello, $GITLAB_USER_LOGIN!"

test-job1:
  stage: test
  script:
    - echo "This job tests something"

test-job2:
  stage: test
  script:
    - echo "This job tests something, but takes more time than test-job1."
    - echo "After the echo commands complete, it runs the sleep command for 20 seconds"
    - echo "which simulates a test that runs 20 seconds longer than test-job1"
    - sleep 20

deploy-prod:
  stage: deploy
  script:
    - echo "This job deploys something from the $CI_COMMIT_BRANCH branch."
  environment: production
```

Pipeline có 3 stage chạy tuần tự **build → test → deploy**. Hai job `test-job1` và `test-job2` cùng stage `test` nên chạy song song. `test-job2` mất lâu hơn khoảng 20 giây do lệnh `sleep 20`.

### Kết quả

**Sơ đồ pipeline #2997080026:** cả 4 job đều Passed.

![Sơ đồ pipeline Phần 1](images/Screenshot%202026-10-28%20084907.png)
<img width="1130" height="856" alt="Screenshot 2026-10-28 084907" src="https://github.com/user-attachments/assets/26cdf399-751c-4c3b-bafa-30738fb96a59" />


**Danh sách job và thời gian chạy:** `test-job2` (30s) chạy lâu hơn `test-job1` (9s), đúng như mong đợi.

![Danh sách job Phần 1](images/Screenshot%202026-10-28%20084923.png)
<img width="1143" height="902" alt="Screenshot 2026-10-28 084923" src="https://github.com/user-attachments/assets/c4666e84-6dd1-4ccf-9fef-953addc37c61" />


**Log job `deploy-prod`:** biến `$CI_COMMIT_BRANCH` được thay bằng `main`.

![Log deploy-prod](images/Screenshot%202026-10-28%20084947.png)
<img width="1138" height="896" alt="Screenshot 2026-10-28 084947" src="https://github.com/user-attachments/assets/688d7c8e-b427-40ef-916e-b2daccd2aa50" />

---

## 4. Phần 2 (6.2.2): Build và deploy Docusaurus lên GitLab Pages

**Project:** `SanoXD322/my-pipeline-tutorial-project`

### 4.1. Chuẩn bị mã nguồn

```powershell
git clone https://gitlab.com/SanoXD322/my-pipeline-tutorial-project.git
cd my-pipeline-tutorial-project

npx create-docusaurus@latest website classic
Get-ChildItem website -Force | Move-Item -Destination . -Force
Remove-Item website -Recurse -Force
```

Chỉnh `docusaurus.config.js` cho khớp với địa chỉ GitLab Pages:

```js
url: 'https://sanoxd322.gitlab.io',
baseUrl: '/my-pipeline-tutorial-project/',
```

```powershell
git add .
git commit -m "Add simple generated Docusaurus site"
git push origin
```

### 4.2. Bước 1: Job thử nghiệm

```yaml
test-job:
  script:
    - echo "This is my first job!"
    - date
```

Log in ra dòng chữ và thời gian hệ thống của runner:

![Log test-job](images/Screenshot%202026-10-28%20095604.png)
<img width="916" height="871" alt="Screenshot 2026-10-28 095604" src="https://github.com/user-attachments/assets/236548d5-3fa4-496f-8670-68ac5d3cd351" />

### 4.3. Bước 2: Job build

```yaml
build-job:
  image: node:lts
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - "build/"
```

Job chạy trong container `node:lts`, cài 1295 gói npm, build thành công (`[SUCCESS] Generated static files in "build"`) và upload 139 file làm artifact:

![Log build-job](images/Screenshot%202026-10-28%20095917.png)
<img width="1220" height="912" alt="Screenshot 2026-10-28 095917" src="https://github.com/user-attachments/assets/52ebd68e-a3ae-46c4-b6da-008192cb6460" />

Nội dung artifact `build/` gồm `index.html`, `404.html`, `sitemap.xml` và các thư mục `assets`, `blog`, `docs`, `img`:

![Artifact build](images/Screenshot%202026-10-28%20095853.png)
<img width="1586" height="878" alt="Screenshot 2026-10-28 095853" src="https://github.com/user-attachments/assets/3f6ca621-5ce7-4459-b4b8-54f92cbe948d" />

### 4.4. Bước 3: Deploy lên GitLab Pages

```yaml
stages:
  - build
  - deploy

build-job:
  stage: build
  image: node:lts
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - "build/"

pages:
  stage: deploy
  script:
    - mv build/ public/
  artifacts:
    paths:
      - "public/"
```

Job `pages` nhận artifact `build/` từ stage trước, đổi tên thành `public/` (thư mục bắt buộc của GitLab Pages). GitLab tự sinh thêm job `pages:deploy` để publish trang.

![Pipeline deploy Pages](images/Screenshot%202026-10-28%20100224.png)
<img width="917" height="598" alt="Screenshot 2026-10-28 100224" src="https://github.com/user-attachments/assets/97944fbe-025f-4a9f-800b-e4e52d45987d" />


Trang **Deploy → Pages** xác nhận bản deploy đang hoạt động (Active), gồm 139 file trong thư mục `/public`:

![Trang quản lý GitLab Pages](images/Screenshot%202026-10-28%20100932.png)
<img width="945" height="757" alt="Screenshot 2026-10-28 100932" src="https://github.com/user-attachments/assets/d45a387e-1526-43eb-899e-323c4fbd1c29" />

Lúc đầu GitLab bật *unique domain* (`my-pipeline-tutorial-project-f5b7d9.gitlab.io`) nên trang bị mất CSS do không khớp `baseUrl`. Sau khi tắt tùy chọn này trong tab **Domains & settings**, trang được phục vụ đúng tại địa chỉ dạng `<username>.gitlab.io/<project>/`.

### 4.5. Kết quả

Trang Docusaurus hiển thị đầy đủ giao diện tại https://sanoxd322.gitlab.io/my-pipeline-tutorial-project/

![Trang Docusaurus trên GitLab Pages](images/Screenshot%202026-10-28%20101211.png)
<img width="1911" height="1005" alt="Screenshot 2026-10-28 101211" src="https://github.com/user-attachments/assets/f5d774f7-2258-4481-b132-39b3bd01a0ec" />

---

## 5. Sự cố gặp phải và cách khắc phục

| Sự cố | Nguyên nhân | Cách khắc phục |
|---|---|---|
| Pipeline đầu tiên **Failed**, báo cần xác minh tài khoản | Instance runner của GitLab.com yêu cầu xác minh danh tính | Dùng project runner tự quản lý chạy bằng Docker trên máy cá nhân |
| Cài Docker Desktop thất bại: thiếu *Virtual Machine Platform* | Tính năng Windows chưa bật, cần quyền Administrator | Chạy `wsl --install` trong PowerShell (Admin), khởi động lại máy |
| `register` báo `Verifying runner... is not valid` | Dùng token mẫu thay vì token thật | Tạo lại runner, copy đúng token `glrt-...` |
| Truy cập Pages báo **401** | Project ở chế độ Private và đang dùng *unique domain* | Đổi project/Pages sang Public, tắt *Use unique domain* |
| Trang hiển thị nhưng **mất CSS** | `baseUrl` không khớp với domain đang truy cập | Tắt unique domain để URL khớp `baseUrl: '/my-pipeline-tutorial-project/'` |

---

## 6. Nhận xét

- Pipeline được định nghĩa hoàn toàn bằng file `.gitlab-ci.yml` trong repository, mỗi lần push lên `main` sẽ tự động build và deploy lại trang web mà không cần thao tác tay.
- **Artifact** là cơ chế truyền kết quả giữa các stage: `build-job` tạo ra `build/`, job `pages` dùng lại mà không phải build lần nữa.
- Log `npm install` báo **25 lỗ hổng** trong các gói phụ thuộc (1 high, 15 critical). Đây là chỗ phần "Sec" của DevSecOps có thể bổ sung, ví dụ thêm template `Jobs/Dependency-Scanning`, `Jobs/SAST` và `Jobs/Secret-Detection` của GitLab vào pipeline để chặn lỗi bảo mật trước khi deploy.
- Runner tự quản lý cho phép chạy CI mà không phụ thuộc runner dùng chung, nhưng máy chạy runner (Docker Desktop) phải luôn bật thì job mới được xử lý.
