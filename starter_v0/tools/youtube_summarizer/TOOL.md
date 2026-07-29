# youtube_summarizer

## Mục đích
Lấy phụ đề (transcript) của một video Youtube bất kỳ dựa trên URL hoặc Video ID, sau đó trích xuất văn bản thô để Agent có thể đọc và tóm tắt nội dung.

## Khi nào dùng
- Khi người dùng cung cấp link Youtube và yêu cầu tóm tắt nội dung, hoặc hỏi thông tin nằm trong video đó.
- KHÔNG dùng cho các nền tảng video khác (Vimeo, Tiktok, Facebook).

## Lưu ý
- Công cụ sử dụng thư viện `youtube-transcript-api` lấy phụ đề tự động (ưu tiên tiếng Việt, sau đó đến tiếng Anh).
- Trả về text nguyên bản, có thể hơi lộn xộn do AI tạo phụ đề. Model cần tự tóm tắt lại.
