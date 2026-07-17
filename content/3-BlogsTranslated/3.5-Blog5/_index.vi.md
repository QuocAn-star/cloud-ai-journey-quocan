---
title: "Blog 5"
date: 2026-01-01
weight: 5
chapter: false
pre: " <b> 3.5. </b> "
---

# Giới thiệu Amazon S3 Object Lambda: Chấm dứt nỗi lo "nhân bản dữ liệu" khi truy xuất từ S3

> **Bài gốc:** [Introducing Amazon S3 Object Lambda – Use Your Code to Process Data as It Is Being Retrieved from S3](https://aws.amazon.com/vi/blogs/aws/introducing-amazon-s3-object-lambda-use-your-code-to-process-data-as-it-is-being-retrieved-from-s3/)

> **Tác giả:** Danilo Poccia

> **Bài dịch:** [Introducing Amazon S3 Object Lambda – Use Your Code to Process Data as It Is Being Retrieved from S3](https://www.facebook.com/groups/awsstudygroupfcj/posts/2198159460949014)

---

Nếu bạn là một Developer hay Data Engineer, chắc hẳn bạn đã từng gặp tình huống oái oăm này: Cùng một tập dữ liệu lưu trữ trên Amazon S3, nhưng ứng dụng phân tích cần che giấu các thông tin nhận dạng cá nhân (PII), trong khi một chiến dịch tiếp thị lại cần chính dữ liệu đó nhưng phải được bổ sung thêm chi tiết từ cơ sở dữ liệu khách hàng.

Việc phải tạo, lưu trữ và duy trì nhiều bản sao dữ liệu tùy chỉnh, hoặc xây dựng một hệ thống proxy trung gian phía trước S3 không chỉ làm tăng độ phức tạp vận hành mà còn gây tốn kém chi phí.

---

## 1. Bước ngoặt mới: Xử lý dữ liệu ngay lập tức với S3 Object Lambda

AWS đã tung ra một tính năng cực kỳ giá trị: **Amazon S3 Object Lambda**, cho phép bạn thêm mã nguồn của riêng mình để tự động xử lý dữ liệu được lấy từ S3 trước khi trả về cho ứng dụng.

Giờ đây, hàm AWS Lambda sẽ được gọi **đồng thời (inline)** với một yêu cầu S3 GET tiêu chuẩn. Bạn không cần phải thay đổi mã của ứng dụng hiện tại mà vẫn có thể dễ dàng trình bày nhiều **góc nhìn (views)** khác nhau từ cùng một tập dữ liệu, và có thể cập nhật hàm Lambda để sửa đổi các góc nhìn này bất kỳ lúc nào.

---

## 2. Tại sao đây là "tin vui" cho các dự án Ứng dụng và Dữ liệu?

| Lợi ích | Mô tả |
|---------|-------|
| **Che giấu dữ liệu nhạy cảm** | Tự động loại bỏ thông tin PII cho môi trường phân tích hoặc phi sản xuất |
| **Linh hoạt chuyển đổi định dạng** | Dễ dàng chuyển đổi định dạng dữ liệu (ví dụ: từ XML sang JSON) hoặc nén/giải nén tệp tin ngay trong lúc tải xuống |
| **Xử lý hình ảnh và tạo dữ liệu động** | Thay đổi kích thước và đóng dấu bản quyền hình ảnh ngay lập tức, hoặc tạo JSON/CSV động dựa trên tên file/HTTP headers mà không cần tệp đó tồn tại sẵn trong S3 |
| **Giảm gánh nặng hạ tầng** | Không còn phải duy trì máy chủ proxy hay quản lý vô số bản sao dữ liệu dư thừa |

---

## 3. Cơ chế hoạt động đằng sau

Sức mạnh của tính năng này nằm ở sự kết hợp giữa các **Điểm truy cập (Access Points)** và một API hoàn toàn mới.

Hàm Lambda **không cần** có quyền đọc trực tiếp từ S3. Thay vào đó, nó nhận được một **URL được ký trước** (`inputS3Url`) từ một Access Point hỗ trợ để tải xuống chính xác đối tượng đang cần xử lý.

Sau khi việc chuyển đổi hoàn tất, hàm Lambda sẽ sử dụng API mới mang tên **`WriteGetObjectResponse`** để gửi lại đối tượng đã sửa đổi cho S3 Object Lambda. Nhờ API này, đối tượng trả về có thể có kích thước lớn hơn rất nhiều so với giới hạn phản hồi thông thường của Lambda và còn hỗ trợ **mã hóa truyền dữ liệu theo khối (chunked transfer encoding)** để truyền dữ liệu dạng luồng.

---

## 4. Lưu ý khi triển khai

| Lưu ý | Chi tiết |
|-------|---------|
| **Cập nhật ứng dụng rất đơn giản** | Chỉ cần thay thế tên S3 bucket bằng ARN của **S3 Object Lambda Access Point** |
| **Thời gian xử lý** | Thời gian chạy tối đa của Lambda được gọi bởi S3 Object Lambda là **60 giây** |
| **Giới hạn CLI** | Các lệnh S3 bậc cao như `aws s3 cp` chưa hỗ trợ S3 Object Lambda - dùng lệnh API bậc thấp như `aws s3api get-object` thay thế |
| **Chi phí** | Tính theo tài nguyên điện toán Lambda, số lượng yêu cầu xử lý, lượng dữ liệu trả về và các yêu cầu S3 gốc do Lambda thực hiện |

---

## Bài học rút ra

- S3 Object Lambda loại bỏ nhu cầu nhân bản dữ liệu - một nguồn, nhiều góc nhìn tùy chỉnh
- Pattern `inputS3Url` giúp Lambda không cần quyền trực tiếp với S3
- `WriteGetObjectResponse` xóa bỏ giới hạn kích thước vốn làm hạn chế tính hữu dụng của Lambda với dữ liệu lớn
- Che PII, chuyển đổi định dạng và xử lý hình ảnh đều là use case "hạng nhất" của tính năng này
- Cập nhật một "góc nhìn" chỉ cần sửa một hàm Lambda - không cần thay đổi pipeline dữ liệu

---

*Hình ảnh minh họa:*

![Blog 5 - Giới Thiệu Amazon S3 Object Lambda](/images/blog5.jpg)