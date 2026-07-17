---
title: "Worklog Tuần 2"
date: 2026-04-27
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
---

**Thời gian:** 27/04/2026 - 01/05/2026

## Mục tiêu tuần 2

- Tìm hiểu các dịch vụ lưu trữ trên nền tảng AWS và vai trò của chúng trong các hệ thống điện toán đám mây.
- Nắm vững các khái niệm cơ bản của Amazon S3 và cách quản lý dữ liệu trên dịch vụ này.
- Thực hành tạo, cấu hình và quản lý S3 Bucket, đồng thời tìm hiểu các cơ chế bảo mật và tối ưu lưu trữ.
- Chuẩn bị kiến thức về lưu trữ dữ liệu phục vụ dự án Data Lakehouse.

### Các công việc cần triển khai trong tuần này

| Thứ | Công việc | Ngày | Nguồn tài liệu |
|:---:|-----------|:----:|----------------|
| **2** | Tìm hiểu tổng quan về Amazon Simple Storage Service (Amazon S3), nghiên cứu kiến trúc lưu trữ đối tượng (Object Storage), cách tạo Bucket và tổ chức dữ liệu trên Amazon S3 để phục vụ lưu trữ dữ liệu cho các ứng dụng trên nền tảng AWS. | 27/04/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html |
| **3** | Nghiên cứu các lớp lưu trữ (Storage Classes) của Amazon S3, tìm hiểu đặc điểm, chi phí và trường hợp sử dụng của từng lớp nhằm lựa chọn phương án lưu trữ phù hợp với từng loại dữ liệu. | 28/04/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html |
| **4** | Tìm hiểu tính năng Versioning trên Amazon S3, nghiên cứu cơ chế quản lý phiên bản của đối tượng và khả năng khôi phục dữ liệu khi xảy ra các thao tác chỉnh sửa hoặc xóa nhầm. | 29/04/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html |
| **5** | Nghiên cứu S3 Lifecycle, tìm hiểu cách tự động chuyển đổi dữ liệu giữa các lớp lưu trữ và thiết lập quy tắc xóa dữ liệu nhằm tối ưu chi phí lưu trữ trên AWS. | 30/04/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html |
| **6** | Tìm hiểu AWS Identity and Access Management (IAM), nghiên cứu cách quản lý người dùng, nhóm, vai trò và chính sách phân quyền để kiểm soát quyền truy cập vào các tài nguyên AWS một cách an toàn. | 01/05/2026 | https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html |


## Kết quả đạt được

- Hiểu được kiến trúc và nguyên lý hoạt động của dịch vụ Amazon S3.
- Hoàn thành việc tạo và quản lý S3 Bucket cũng như các Object trên AWS.
- Thiết lập được các chính sách bảo mật và quyền truy cập cho Amazon S3.
- Thực hành thành công các tính năng Versioning và Lifecycle Rule nhằm tối ưu việc lưu trữ dữ liệu.
- Nắm được các nguyên tắc và Best Practices trong quản lý dữ liệu trên Amazon S3, tạo nền tảng cho việc triển khai hệ thống Data Lakehouse ở các giai đoạn tiếp theo.