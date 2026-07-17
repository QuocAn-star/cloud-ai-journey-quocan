---
title: "Blog 2"
date: 2026-01-01
weight: 2
chapter: false
pre: " <b> 3.2. </b> "
---

# Quản lý dữ liệu trên AWS: Chấm dứt nỗi lo "phân quyền hai nơi" cho S3 và Lake Formation

> **Bài gốc:** [Access Amazon S3 Data Files Directly Using AWS Lake Formation Permissions](https://aws.amazon.com/blogs/big-data/access-amazon-s3-data-files-directly-using-aws-lake-formation-permissions/)

> **Tác giả:** Aarthi Srinivasan, Archana Inapudi, Anandkumar Kaliaperumal, Mitali Sheth, and Srinivasan Krishnasamy

> **Bài dịch:** [Access Amazon S3 Data Files Directly Using AWS Lake Formation Permissions](https://www.facebook.com/groups/awsstudygroupfcj/permalink/2189246758506951/?rdid=ns4Quvh0bISXoSAa#)

---

Nếu bạn là một Data Scientist hay ML Engineer, chắc hẳn bạn đã từng gặp tình huống oái oăm này: Bạn có quyền truy cập vào bảng dữ liệu qua SQL, nhưng khi cần đọc file thô từ Amazon S3 để huấn luyện mô hình, bạn lại bị từ chối vì thiếu quyền trong S3 bucket policy.

Việc phải duy trì song song hai hệ thống chính sách - một bên là Lake Formation cho bảng, một bên là IAM/S3 cho tệp - không chỉ gây tốn thời gian mà còn tiềm ẩn rủi ro **sai lệch quyền hạn (permission drift)**.

---

## 1. Bước ngoặt mới: Hợp nhất quyền truy cập

AWS vừa tung ra một tính năng cực kỳ giá trị: **Truy cập trực tiếp các tệp dữ liệu trên S3 bằng chính quyền hạn của AWS Lake Formation**.

Giờ đây, thay vì chỉ có thể dùng lệnh `spark.sql()`, các nhà khoa học dữ liệu có thể trực tiếp sử dụng các hàm lập trình quen thuộc như `spark.read.parquet()` hoặc `spark.read.csv()` trên **Amazon EMR** hay **SageMaker** mà vẫn tuân thủ đúng các quy tắc bảo mật đã thiết lập trong Lake Formation. Mọi quyền hạn hiện nay đều được quản trị tập trung tại **một nơi duy nhất**.

---

## 2. Tại sao đây là "tin vui" cho các dự án AI và Data?

Tính năng này mang lại **4 lợi ích cốt lõi** giúp tối ưu hóa quy trình làm việc:

| Lợi ích | Mô tả |
|---------|-------|
| **Hệ thống phân quyền thống nhất** | Truy vấn bảng bằng Athena (SQL) và đọc/ghi file S3 bằng Spark (Programmatic API) chỉ cần một bộ quyền duy nhất |
| **Sẵn sàng cho Generative AI** | Các pipeline ML giờ đây có thể đọc dữ liệu huấn luyện trực tiếp từ data lake có quản trị, đẩy nhanh tốc độ xây dựng mô hình |
| **Giảm gánh nặng vận hành** | Đội ngũ Operations không còn phải duy trì các chính sách IAM phức tạp cho từng bucket S3 |
| **Kiểm toán dễ dàng hơn** | Mọi hoạt động truy cập (cả SQL lẫn trực tiếp qua file) đều được ghi lại thống nhất trong AWS CloudTrail |

---

## 3. Cơ chế hoạt động đằng sau

Sức mạnh của tính năng này nằm ở một API mới mang tên **`GetTemporaryDataLocationCredentials()`**, giúp cấp các thông tin xác thực tạm thời dựa trên quyền hạn của người dùng đối với các bảng trong **AWS Glue Data Catalog**. AWS cũng cung cấp một **plugin Java** đặc biệt để tự động hóa việc kiểm tra quyền và cấp credentials mà người dùng không cần phải can thiệp thủ công vào code.

---

## 4. Một vài lưu ý khi triển khai

Để bắt đầu sử dụng, bạn cần lưu ý các điều kiện kỹ thuật sau:

- **Quyền hạn**: Người dùng cần có quyền `SELECT` trên toàn bộ các hàng và cột của bảng để có thể truy cập file trực tiếp.
- **Phiên bản hỗ trợ**: Yêu cầu **Amazon EMR 7.13+**, **Boto3 1.42.29+** và **AWS CLI 2.33.1+**.
- **Giới hạn định dạng**: Định dạng bảng **Apache Iceberg** hiện chưa được hỗ trợ bởi plugin này.

---

## Bài học rút ra

- Một hệ thống phân quyền duy nhất - không còn phải bảo trì song song giữa Lake Formation và S3 bucket policy
- `GetTemporaryDataLocationCredentials()` là API làm nên sự khác biệt
- Đây là tính năng cần thiết cho các team ML đang xây dựng training pipeline trên data lake có quản trị
- Audit trail được thống nhất - các team tuân thủ sẽ thực sự trân trọng điều này

---

*Hình ảnh minh họa:*

![Blog 2 - Hợp Nhất Quyền S3 & Lake Formation](/images/blog2.jpg)