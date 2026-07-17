---
title: "Blog 4"
date: 2026-01-01
weight: 4
chapter: false
pre: " <b> 3.4. </b> "
---

# Tự động hóa nâng cấp Amazon Aurora PostgreSQL: Giảm 80% gánh nặng cho DBA

> **Bài gốc:** [Automate Amazon Aurora PostgreSQL Major or Minor Version Upgrade Using AWS Systems Manager and Amazon EC2](https://aws.amazon.com/blogs/database/automate-amazon-aurora-postgresql-major-or-minor-version-upgrade-using-aws-systems-manager-and-amazon-ec2/)

> **Tác giả:** Rajeev Pardipuram, Anand Komandooru, Sameer Kumar, and Li Liu

> **Bài dịch:** [Automate Amazon Aurora PostgreSQL Major or Minor Version Upgrade Using AWS Systems Manager and Amazon EC2](https://www.facebook.com/groups/awsstudygroupfcj/permalink/2181404265957867/?rdid=g9DRm6bfvHIxjqpG#)

---

Việc quản lý và nâng cấp các phiên bản lớn (major) hay nhỏ (minor) cho hàng loạt cụm cơ sở dữ liệu Amazon Aurora PostgreSQL chưa bao giờ là công việc dễ dàng. Nếu thực hiện thủ công, bạn không chỉ tốn hàng giờ đồng hồ mà còn đối mặt với rủi ro sai sót cấu hình rất lớn.

Bài viết này chia sẻ một giải pháp **tự động hóa toàn diện** giúp tối ưu hóa quy trình này, dựa trên sự kết hợp giữa **AWS Systems Manager** và **Amazon EC2**.

---

## 1. Tại sao bạn nên quan tâm đến giải pháp này?

Điểm nổi bật nhất của giải pháp chính là khả năng **giảm tới 80% nỗ lực thủ công**. Thay vì phải đăng nhập vào từng cluster, bạn giờ đây có thể điều phối việc nâng cấp cho toàn bộ "hạm đội" cơ sở dữ liệu của mình một cách nhất quán và an toàn.

Đặc biệt, giải pháp này tận dụng tính năng **Copy-on-Write cloning** của Aurora. Trước khi thực hiện bất kỳ thay đổi nào trên dữ liệu thật, hệ thống sẽ tạo một bản sao cực nhanh để đảm bảo bạn luôn có một "lưới an toàn" nếu có sự cố xảy ra.

---

## 2. "Bộ khung" của hệ thống tự động hóa

Đây không chỉ là một tập lệnh đơn lẻ, mà là một quy trình khép kín sử dụng các dịch vụ cốt lõi của AWS:

| Dịch vụ | Vai trò |
|---------|---------|
| **AWS Systems Manager** | "Nhạc trưởng" - điều phối toàn bộ công việc |
| **Amazon EC2** | Thực thi các script tự động hóa và lệnh CLI |
| **AWS Secrets Manager** | Lưu trữ an toàn mật khẩu quản trị của DB |
| **Amazon S3** | Lưu trữ log chi tiết từ mỗi lần nâng cấp |
| **Amazon SNS** | Gửi email thông báo ngay khi quá trình hoàn tất |

---

## 3. Quy trình hoạt động trong 2 giai đoạn

Hệ thống sử dụng **thẻ (tags)** làm cơ chế kích hoạt - bạn chỉ cần gắn tag `"UpgradeDB: Y"` vào các cluster muốn nâng cấp, hệ thống tự động nhận diện. Quy trình gồm hai giai đoạn:

### Giai đoạn 1: PREUPGRADE (Tiền nâng cấp)
Đây là bước cực kỳ quan trọng. Hệ thống sẽ:
- Kiểm tra trạng thái replication slots
- Thực hiện các tác vụ `VACUUM`
- Báo cáo xem DB của bạn đã sẵn sàng để lên đời hay chưa

### Giai đoạn 2: UPGRADE (Nâng cấp thực tế)
Sau khi đã kiểm tra kỹ, bạn kích hoạt chế độ này để hệ thống:
- Tiến hành nâng cấp phiên bản engine
- Cập nhật các tiện ích mở rộng (extensions)
- Thực hiện lệnh `ANALYZE` để tối ưu hóa hiệu suất ngay sau nâng cấp

---

## 4. Khả năng giám sát tuyệt vời

Một trong những điểm hay nhất ở giải pháp này là **hệ thống nhật ký (logging) rất chi tiết**. Mọi hành động từ lúc tạo clone, sao lưu cấu hình cho đến kết quả cập nhật từng extension đều được ghi lại và đẩy lên S3.

Nếu một cụm nào đó gặp lỗi, bạn sẽ biết chính xác nguyên nhân nằm ở đâu để xử lý **mà không ảnh hưởng đến các cụm khác**.

---

## 5. Lời kết

Nếu bạn đang quản lý một hệ thống dữ liệu lớn trên AWS, việc chuyển từ nâng cấp thủ công sang tự động hóa là bước đi tất yếu. Nó không chỉ giúp bạn "ngủ ngon hơn" mỗi khi đến kỳ bảo trì mà còn đảm bảo tính ổn định tối đa cho ứng dụng.

Hãy bắt đầu bằng cách thử nghiệm trong môi trường phi sản xuất trước, sau đó mới triển khai rộng rãi.

---

## Bài học rút ra

- Cơ chế kích hoạt bằng tag (`UpgradeDB: Y`) đơn giản và có thể mở rộng rất dễ dàng
- Copy-on-Write cloning cung cấp lưới an toàn với hầu như không tác động đến hiệu năng
- Thiết kế hai giai đoạn (PREUPGRADE → UPGRADE) ngăn ngừa các sự cố bất ngờ trong quá trình nâng cấp thật
- Logging tập trung trên S3 cho phép kiểm tra lịch sử toàn bộ hành động trên mọi cluster

---

*Hình ảnh minh họa:*

![Blog 4 - Tự Động Hóa Nâng Cấp Aurora PostgreSQL](/images/blog4.jpg)