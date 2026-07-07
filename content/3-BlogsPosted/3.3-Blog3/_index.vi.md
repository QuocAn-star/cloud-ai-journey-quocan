---
title: "Blog 3"
date: 2026-01-01
weight: 3
chapter: false
pre: " <b> 3.3. </b> "
---

# Di chuyển dữ liệu và tiết kiệm chi phí ở quy mô lớn với Amazon S3 File Gateway

> **Bài gốc:** [Data Migrations at Scale with Amazon S3 File Gateway](https://aws.amazon.com/vi/blogs/storage/data-migrations-at-scale-with-amazon-s3-file-gateway)

> **Bài dịch:** [Data Migrations at Scale with Amazon S3 File Gateway](https://www.facebook.com/photo/?fbid=1029722426099971&set=gm.2200052700759690&idorvanity=660548818043427)

---

Nếu bạn đang quản lý hệ thống máy chủ lưu trữ nội bộ (on-premises) và muốn di chuyển một lượng lớn dữ liệu lên đám mây, chắc hẳn bạn đã hoặc sẽ gặp phải bài toán này: **Làm sao để di chuyển mà vẫn giữ nguyên cấu trúc cũng như ngày giờ tạo gốc của các tệp tin?**

Việc dữ liệu bị "làm mới" thời gian lúc tải lên đám mây không chỉ làm mất đi thông tin lịch sử quan trọng mà còn tước đi cơ hội tận dụng các chính sách tự động phân tầng để tiết kiệm chi phí cho những dữ liệu đã cũ.

---

## 1. Vấn đề: Mất metadata khi di chuyển dữ liệu

Khi di chuyển dữ liệu lên Amazon S3 thông qua **S3 File Gateway**, hệ thống sẽ tự động lấy **Ngày sửa đổi (Modified Date)** từ tệp nguồn để gán thành **Ngày tạo (Create Date)** mới trên S3.

Sự thay đổi này làm tuổi thọ của tệp bị "reset", khiến các **Chính sách Vòng đời (S3 Lifecycle Policy)** không thể tự động phân loại và đẩy những dữ liệu cũ vào các lớp lưu trữ giá rẻ dựa trên tuổi đời thật của chúng - gây lãng phí ngân sách lưu trữ của doanh nghiệp.

---

## 2. Giải pháp: Tự động hóa bảo toàn siêu dữ liệu

Thay vì để AWS làm mới thời gian, bạn có thể kết hợp **Robocopy**, **Amazon S3 File Gateway** và **AWS Lambda** để di chuyển dữ liệu mà vẫn giữ nguyên vẹn các siêu dữ liệu (metadata) ban đầu.

Hàm Lambda sẽ tự động đọc ngày tháng thực sự của tệp và chuyển chúng vào đúng lớp lưu trữ phù hợp (như **Glacier Instant Retrieval** hay **Glacier Deep Archive**) ngay khi dữ liệu vừa hạ cánh lên S3.

---

## 3. Tại sao đây là giải pháp tối ưu?

| Lợi ích | Mô tả |
|---------|-------|
| **Bảo toàn thông tin gốc** | Giữ nguyên thời gian tạo, sửa đổi và các quyền truy cập NTFS gốc của tệp trong quá trình chuyển đổi |
| **Tối ưu chi phí ở quy mô lớn** | Tự động đẩy các tệp tin cũ vào lớp lưu trữ S3 chi phí thấp dựa trên tuổi thọ *thật sự* của chúng, không phải ngày tải lên đám mây |
| **Hỗ trợ kiến trúc lai (Hybrid Cloud)** | Doanh nghiệp vẫn có thể truy cập dữ liệu đám mây từ ứng dụng on-premises qua SMB và NFS mà không cần thay đổi môi trường hiện tại |
| **Tự động hóa hoàn toàn** | Tận dụng tích hợp sâu của Lambda với S3 để tự động thực thi chuyển đổi lớp lưu trữ mà không cần can thiệp thủ công |

---

## 4. Cơ chế hoạt động: 3 thành phần chính

**Robocopy:**
Sử dụng công cụ này với các tham số chuyên dụng (như `/TIMEFIX` để đồng bộ thời gian, `/SECFIX` để sao chép quyền truy cập) để chép dữ liệu vào file share của S3 File Gateway nhằm giữ lại các thuộc tính gốc.

**Amazon S3 File Gateway:**
Khi tự động đưa tệp lên S3, gateway sẽ lưu trữ thời gian gốc (thông số `mtime`) dưới dạng **siêu dữ liệu do người dùng xác định (user-defined metadata)** đính kèm vào các object trên S3.

**AWS Lambda:**
Bất cứ khi nào có lệnh `PUT` để ghi một object lên S3, Lambda sẽ được kích hoạt, trích xuất thông số `mtime` (định dạng Unix time) từ siêu dữ liệu và gọi API để chuyển tệp sang lớp lưu trữ chi phí thấp nếu đạt đủ điều kiện về tuổi thọ.

---

## 5. Lưu ý khi triển khai

- **Cẩn trọng với tốc độ Robocopy**: Quá trình sao chép có thể chậm tùy thuộc vào số lượng tệp và tốc độ ổ cứng. Dùng cờ `/L` (dry run) để xem trước các thay đổi trước khi sao chép thật.
- **Lựa chọn nền tảng cho File Gateway**: S3 File Gateway hỗ trợ chạy dưới dạng máy ảo (VMware, Microsoft Hyper-V, Linux KVM) hoặc thiết bị phần cứng chuyên dụng tại trung tâm dữ liệu.

---

## Bài học rút ra

- Bảo toàn metadata khi di chuyển lên đám mây không chỉ là "tính năng thêm" - nó ảnh hưởng trực tiếp đến chi phí lưu trữ
- Trường `mtime` được lưu dưới dạng S3 object metadata là chìa khóa để kích hoạt lifecycle policy dựa trên tuổi thật của file
- Mô hình ba thành phần (Robocopy + S3 File Gateway + Lambda) có thể tái sử dụng cho bất kỳ dự án di chuyển on-premises lên cloud nào
- Chế độ `/L` dry-run của Robocopy là người bạn tốt nhất trước khi chạy migration thật

---

*Hình ảnh minh họa:*

![Blog 3 - Di Chuyển Dữ Liệu Quy Mô Lớn với S3 File Gateway](/images/blog3.jpg)
