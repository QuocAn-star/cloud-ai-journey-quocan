---
title: "Blog 5"
date: 2026-06-27
weight: 5
chapter: false
pre: " <b> 3.5. </b> "
---

# Introducing Amazon S3 Object Lambda: Ending the "Data Duplication" Problem When Retrieving from S3

> **Original article:** [Introducing Amazon S3 Object Lambda – Use Your Code to Process Data as It Is Being Retrieved from S3](https://aws.amazon.com/vi/blogs/aws/introducing-amazon-s3-object-lambda-use-your-code-to-process-data-as-it-is-being-retrieved-from-s3/)

> **Translation:** [Introducing Amazon S3 Object Lambda – Use Your Code to Process Data as It Is Being Retrieved from S3](https://www.facebook.com/groups/awsstudygroupfcj/posts/2198159460949014)

---

If you're a Developer or Data Engineer, you've likely encountered this frustrating scenario: The same dataset stored in Amazon S3, but your analytics application needs PII masked, while a marketing campaign needs the same data enriched with details from a customer database.

Creating, storing, and maintaining multiple customized data copies for each application - or building and managing an S3 proxy layer - adds operational complexity and drives up costs unnecessarily.

---

## 1. The New Breakthrough: Process Data Instantly with S3 Object Lambda

AWS has introduced an extremely valuable feature: **Amazon S3 Object Lambda**, which lets you add your own code to automatically process data retrieved from S3 before it's returned to the application.

Now, an AWS Lambda function is invoked **inline** with a standard S3 GET request. You don't need to change your application code - you can easily present multiple **views** from the same dataset and update the Lambda function to modify those views at any time.

---

## 2. Why This Is Great News for Application and Data Projects

| Benefit | Description |
|---------|-------------|
| **Mask sensitive data** | Automatically remove PII for analytics or non-production environments |
| **Flexible format conversion** | Convert data formats (e.g., XML to JSON) or compress/decompress files on the fly during download |
| **Image processing & dynamic data generation** | Resize and watermark images on-the-fly based on caller information, or generate dynamic JSON/CSV files based on filename or HTTP headers - without needing the file to pre-exist in S3 |
| **Reduced infrastructure burden** | Development teams no longer need to maintain proxy servers or manage countless redundant data copies |

---

## 3. The Mechanism Under the Hood

The power of this feature lies in the combination of **Access Points** and a brand-new API.

The Lambda function does **not** need direct read permissions from S3. Instead, it receives a **pre-signed URL** (`inputS3Url`) from a supporting Access Point to download exactly the object being processed.

After the transformation is complete, the Lambda function uses the new **`WriteGetObjectResponse`** API to send the modified object back to S3 Object Lambda. This API allows the returned object to be much larger than a standard Lambda response limit and also supports **chunked transfer encoding** for streaming data.

---

## 4. Key Notes for Deployment

| Note | Details |
|------|---------|
| **Updating applications is simple** | Just replace the S3 bucket name with the ARN of the **S3 Object Lambda Access Point** |
| **Processing time limit** | Maximum duration for a Lambda function invoked by S3 Object Lambda is **60 seconds** |
| **CLI support limitation** | High-level S3 CLI commands like `aws s3 cp` don't support S3 Object Lambda objects - use lower-level API commands like `aws s3api get-object` instead |
| **Pricing** | Charged based on Lambda compute resources, number of data processing requests, data returned to the application, and underlying S3 requests made by Lambda |

---

## Key Takeaways

- S3 Object Lambda eliminates the need for data duplication - one source, multiple tailored views
- The `inputS3Url` pattern keeps Lambda decoupled from direct S3 permissions
- `WriteGetObjectResponse` removes the size constraint that would otherwise limit Lambda's usefulness for large objects
- PII masking, format conversion, and image processing are all first-class use cases
- Updating a "view" is as simple as updating one Lambda function - no data pipeline changes needed

---

*Blog image:*

![Blog 5 - Introducing Amazon S3 Object Lambda](/images/blog5.jpg)