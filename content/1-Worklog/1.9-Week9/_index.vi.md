---
title: "Worklog Tuần 9"
date: 2026-06-22
weight: 9
chapter: false
pre: " <b> 1.9. </b> "
---

**Thời gian:** 15/06/2026 - 19/06/2026

## Mục tiêu tuần 9

- Phát triển Dashboard trực quan hóa dữ liệu bằng Streamlit.
- Kết nối Dashboard với Amazon Athena để truy vấn dữ liệu.
- Xây dựng các biểu đồ và chỉ số phục vụ phân tích hành vi khách hàng.
- Hoàn thiện giao diện Dashboard phục vụ việc theo dõi và ra quyết định.

### Các công việc cần triển khai trong tuần này

| Thứ | Công việc | Ngày | Nguồn tài liệu |
|:---:|-----------|:----:|----------------|
| **2** | Tìm hiểu Streamlit và xây dựng cấu trúc ban đầu của Dashboard, thiết kế giao diện hiển thị các chỉ số phân tích, đồng thời cấu hình môi trường phát triển để kết nối với các dịch vụ AWS. | 15/06/2026 | https://docs.streamlit.io/ |
| **3** | Kết nối Dashboard với Amazon Athena thông qua AWS SDK for pandas (AWS Wrangler), thực hiện truy vấn dữ liệu từ các bảng trong Gold Layer và kiểm tra khả năng đọc dữ liệu để phục vụ trực quan hóa. | 16/06/2026 | https://aws-sdk-pandas.readthedocs.io/en/stable/ |
| **4** | Xây dựng các biểu đồ trực quan như doanh thu theo ngày, doanh thu theo quốc gia, phân bố thiết bị truy cập, phương thức thanh toán và các chỉ số KPI nhằm hỗ trợ phân tích hành vi khách hàng. | 17/06/2026 | https://plotly.com/python/ |
| **5** | Hoàn thiện giao diện Dashboard bằng Streamlit, sắp xếp bố cục các biểu đồ và KPI, tối ưu khả năng hiển thị và kiểm tra tính chính xác của dữ liệu được trình bày trên Dashboard. | 18/06/2026 | https://docs.streamlit.io/develop/api-reference |
| **6** | Kiểm thử toàn bộ Dashboard, đánh giá hiệu năng truy vấn dữ liệu từ Amazon Athena, rà soát các lỗi phát sinh và hoàn thiện ứng dụng trước khi triển khai trên Amazon EC2. | 19/06/2026 | https://docs.streamlit.io/develop/concepts |


## Kết quả đạt được

- Hoàn thành xây dựng Dashboard trực quan hóa dữ liệu bằng Streamlit.
- Kết nối thành công Dashboard với Amazon Athena để truy vấn dữ liệu.
- Xây dựng các biểu đồ và KPI phục vụ phân tích hành vi khách hàng.
- Hoàn thiện giao diện Dashboard với khả năng hiển thị trực quan và dễ sử dụng.
- Chuẩn bị Dashboard sẵn sàng cho giai đoạn triển khai trên Amazon EC2.