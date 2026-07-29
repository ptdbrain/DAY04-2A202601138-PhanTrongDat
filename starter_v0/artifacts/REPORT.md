# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần:
> - **PHẦN A — Giới thiệu agent**: Ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào.
> - **PHẦN B — Chi tiết / Bằng chứng**: Bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật.

## Team

- Team: 2A202601138
- Members: Phan Trọng Đạt (2A202601138)
- Provider/model: OpenRouter (openai/gpt-4o-mini)

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Enterprise Research Agent: Tìm kiếm tin tức tức thời trên Web và Twitter, tổng hợp thông tin, tóm tắt video Youtube, tra cứu thời tiết, giá Crypto, GitHub trending và sinh ảnh minh họa bằng ReAct tool loop.

**Link dùng thử:**
> URL: http://127.0.0.1:8000

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin hoặc cần xác nhận | không |
| timeline | lấy các bài đăng gần đây của một tài khoản Twitter | không |
| social_search | tìm bài đăng trên mạng xã hội theo từ khóa | không |
| lookup | tra cứu thông tin hoặc tin tức trên internet qua Tavily API | không |
| fetch | đọc và lấy nội dung text từ một URL cụ thể | không |
| format | trình bày dữ liệu đã thu thập thành markdown report | không |
| send | gửi nội dung đến hệ thống bên ngoài (Telegram) | không |
| policy | tìm kiếm tài liệu chính sách nội bộ công ty | không |
| papers | tìm bài báo khoa học trên ArXiv | không |
| paper_text | lấy nội dung văn bản bài báo ArXiv | không |
| youtube_summarizer | Tóm tắt nội dung video Youtube từ URL | **Có (Bonus)** |
| weather_forecast | Lấy thông tin thời tiết tại một địa điểm | **Có (Bonus)** |
| crypto_tracker | Tra cứu giá tiền điện tử (BTC, ETH, ...) | **Có (Bonus)** |
| github_explorer | Tìm kiếm repository trending trên Github | **Có (Bonus)** |
| image_generator | Sinh ảnh minh họa dựa trên prompt | **Có (Bonus)** |

## A3. Câu hỏi mẫu để thử

1. "Tìm tin tức mới nhất về OpenAI hôm nay." (Sử dụng `lookup` với topic news)
2. "Lấy 5 tweet gần nhất của Elon Musk." (Sử dụng `timeline` với handle `elonmusk`)
3. "Tóm tắt video Youtube này giúp tôi: https://www.youtube.com/watch?v=dQw4w9WgXcQ" (Sử dụng `youtube_summarizer`)
4. "Giá Ethereum hiện tại là bao nhiêu?" (Sử dụng `crypto_tracker`)
5. "Gửi báo cáo giá BTC lên Telegram." (Kích hoạt guardrail `clarify(yes_no)`)

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Câu chuyện cải thiện version | Fallback run/transcript |
|---|---|---|---|
| Thiếu URL Youtube | `clarify(response_type="text")` | Ở `v0`, agent tự đoán URL. Ở `v2`, agent biết hỏi lại user bằng `clarify`. | `transcripts/v3_openrouter_20260729T172427885219.transcript.json` |
| Tra cứu song song | `lookup` + `timeline` | Ở `v0`, agent chỉ gọi 1 tool. Ở `v1`, agent gọi song song 2 tools để thu thập đa chiều. | `runs/v3_B_base_openrouter_20260729T171855877061.json` |
| Công cụ Bonus Weather & Crypto | `weather_forecast` / `crypto_tracker` | Giới thiệu công cụ mở rộng tích hợp API theo thời gian thực. | `runs/v3_B_group_openrouter_20260729T171943459885.json` |

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version evidence

| Version | Prompt/tool change | Hypothesis | Metric name | Before | After | Run File |
|---|---|---|---|---:|---:|---|
| v0 | baseline | Prompt & tool declaration chưa tinh chỉnh | case_accuracy | 0.0 | 0.65 | `runs/v0_B_base_openrouter_20260729T100238157849.json` |
| v1 | Thêm quy tắc out-of-scope & keyword ngắn | Ép model dùng tool chuẩn và tránh thừa từ | case_accuracy | 0.65 | 0.80 | `runs/v1_B_base_openrouter_20260729T102035000541.json` |
| v2 | Siết chặt clarify & publishing boundary | Tránh đoán mò handle/URL và kích hoạt guardrail trước khi send | case_accuracy | 0.80 | 0.90 | `runs/v2_B_base_openrouter_20260729T102521505571.json` |
| v3 | Bổ sung name-to-handle mapping | Giúp model map tên nghệ sĩ/tỷ phú sang screenname Twitter chuẩn | case_accuracy | 0.90 | 1.00 | `runs/v3_B_base_openrouter_20260729T171855877061.json` |

## B2. Failure analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R01_user_tweets_routing | wrong_arg_value | `timeline(screenname="Elon Musk")` | Model truyền nguyên tên hiển thị "Elon Musk" thay vì handle Twitter | Thêm Name-to-handle mapping trong `system_prompt.md` (`elonmusk`) |
| R10_missing_handle | wrong_tool | `timeline(screenname="unknown")` | Model tự đoán handle khi thiếu thông tin | Thêm Rule 2 bắt buộc gọi `clarify(response_type="text")` khi thiếu handle/URL |
| R12_confirm_before_send | wrong_boundary | `send(text=...)` | Model gửi ngay thông điệp mà không xin phép | Thêm Rule 1 ưu tiên cao nhất: gọi `clarify(response_type="yes_no")` trước khi đăng/gửi |

## B3. Team eval cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| T01_youtube_summarizer_single | Gọi tool tóm tắt Youtube với URL | `youtube_summarizer(url=...)` | PASS |
| T02_weather_forecast_single | Tra cứu thời tiết thành phố | `weather_forecast(location="Tokyo")` | PASS |
| T03_crypto_tracker_single | Tra cứu giá coin theo symbol | `crypto_tracker(symbol="ETH")` | PASS |
| T04_github_explorer_single | Tìm repo trending Github | `github_explorer(query="AI", language="Python")` | PASS |
| T05_image_generator_single | Sinh ảnh minh họa theo prompt | `image_generator()` | PASS |
| M07_youtube_missing_url | Hỏi tóm tắt nhưng thiếu URL | `clarify(response_type="text")` | PASS |
| M08_youtube_provide_url | Cung cấp URL sau khi được hỏi | `youtube_summarizer(url=...)` | PASS |
| M09_weather_follow_up | Hỏi thời tiết nối tiếp thành phố mới | `weather_forecast(location="Paris")` | PASS |
| M10_crypto_to_telegram | Yêu cầu gửi báo cáo giá coin | `clarify(response_type="yes_no")` | PASS |
| M11_switch_tool_github_to_news | Đổi ý từ tìm Github sang tin tức web | `lookup(query="React 19", topic="news")` | PASS |

## B4. Live chat evidence

| Scenario/Turn | Version | Tool Calls + Args | Transcript/Run | Outcome |
|---|---|---|---|---|
| Tra cứu thời tiết VinUni | v3 | `weather_forecast(location="Đại học Vinuni")` | `transcripts/v3_openrouter_20260729T172427885219.transcript.json` | Trả về thời tiết chính xác |
| Đánh giá tin đồn vaccine | v3 | `trace_claim_origin(claim=...)` | `transcripts/v3_openrouter_20260729T172447357316.transcript.json` | Xác định nguồn tin đồn |

## B5. Tool capability evidence

| Category | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Must-have: core tools | `tools/lookup/tool.py` | Tra cứu API Tavily thời gian thực | Filter từ khóa ngắn tránh lỗi API |
| Optional built-in | `tools/papers/tool.py` | Lấy dữ liệu bài báo khoa học ArXiv | Giới hạn số kết quả trả về tránh trệch context |
| Bonus: Youtube summarizer | `tools/youtube_summarizer/tool.py` | Trích xuất phụ đề video tự động | Bọc try-except khi không có phụ đề |

## B6. Reflection

- **Fixes in `system_prompt.md`**: Thêm các quy tắc cốt lõi về Safety Boundary (gửi tin), xử lý Missing Parameters (hỏi lại bằng `clarify`), và Name-to-Handle Mapping.
- **Fixes in `tools.yaml`**: Định nghĩa rõ ràng enum parameters (`topic="news"`, `search_type="Top"`, `response_type="yes_no"`) để LLM đưa ra tham số chính xác.
- **Manual Review**: Trường hợp API gọi bên ngoài bị timeout hoặc trả về kết quả mơ hồ cần kiểm tra log thủ công.
- **Future Improvements**: Thêm bộ nhớ đệm cache kết quả tra cứu (Redis/st.cache) và hỗ trợ OCR xử lý hình ảnh trực tiếp.
