# Tool Setup Guide

Tài liệu này dành cho `starter_v0/`. Tất cả key đặt trong `starter_v0/.env`; không commit, chụp màn hình, hoặc đưa `.env` vào file nộp bài.

Pricing, quota và endpoint có thể thay đổi. Kiểm tra lại trang provider trước mỗi cohort.

## 1. Chuẩn bị môi trường

Chạy từ thư mục gốc repo.

macOS/Linux:

```bash
cd starter_v0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
test -f .env || cp .env.example .env
```

Windows PowerShell:

```powershell
cd starter_v0
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Không ghi đè `.env` nếu file đã tồn tại. Mở `.env`, điền key của provider/tool mà nhóm thực sự dùng, rồi lưu trước khi chạy preflight hoặc smoke test.

Các lệnh bên dưới dùng tên tool ban đầu trong starter. Nếu nhóm đã rename tool, thay key trong `TOOL_FUNCTIONS` bằng tên mới của nhóm.

## 2. Model provider

Khuyến nghị OpenRouter:

```bash
OPENROUTER_API_KEY=...
```

Hoặc chọn một provider khác:

```bash
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...
```

Nếu chọn provider khác, thay `--provider openrouter` bằng provider đó trong **tất cả** lệnh `preflight_provider.py`, `run_eval.py` và `chat.py`.

Preflight:

```bash
python scripts/preflight_provider.py --provider openrouter
```

Preflight chỉ kiểm tra model provider có trả structured tool call. Nó không kiểm tra Tavily, Firecrawl, RapidAPI, arXiv hoặc Telegram; dùng các smoke test bên dưới cho từng tool API.

## 3. Gate matrix

| Capability | Quicktest bắt buộc? | Ghi chú |
|---|---|---|
| Provider + core APIs dùng trong base eval | Có | Phải pass trước khi chạy eval. |
| Tool mới đầu tiên do team viết | Có | Quicktest bằng gọi tool trực tiếp. |
| Tool mới bổ sung để lấy bonus | Khi claim bonus | Phải có quicktest và evidence như tool bắt buộc. |
| UI | Có | Mở được và chạy được luồng demo chính. |
| Optional built-ins (`policy`, `papers`, `paper_text`, `send`) | Chỉ khi demo/dùng | Fail ở đây không chặn core; trong eval để Telegram creds unset. |
| Extension suite | Không | Chỉ chạy khi team chọn dùng optional built-ins. |

Optional quicktest fail không chặn core nếu tool không xuất hiện trong base/group/demo. Tuy nhiên, declaration còn trong `tools.yaml` vẫn được gửi cho model; gọi nhầm optional tool vẫn là lỗi routing core.

Nếu cần strict isolation, bỏ declaration optional không dùng khỏi `tools.yaml` và mention tương ứng trong prompt; giữ implementation/registry, và không chạy extension cho đến khi bật lại.

## 4. Quy tắc đọc smoke test

Mỗi lệnh:

- nạp `.env` trước khi import registry;
- gọi implementation thật qua `TOOL_FUNCTIONS`;
- in `error`, `message` và một summary ngắn;
- không index thẳng `items[0]` khi response có thể rỗng.

Research tool chỉ PASS khi `error` là `None` và có kết quả mong đợi. Telegram dry-run chỉ PASS khi `status` là `needs_confirmation`.

Smoke test có thể tiêu quota API. Chỉ chạy tool nhóm thực sự dùng.

### Core smoke test cho tool mới bắt buộc

Sau khi thêm `TOOL.md`, implementation, registry và declaration YAML, gọi tool trực tiếp bằng input demo an toàn:

```bash
python -c "from pathlib import Path; from env_loader import load_lab_env; load_lab_env(Path.cwd()); from tools import TOOL_FUNCTIONS as T; r=T['YOUR_TOOL_NAME'](**{'YOUR_ARG':'DEMO_VALUE'}); print({'error':r.get('error') if isinstance(r, dict) else None, 'result_type':type(r).__name__})"
```

Thay tên/args theo tool của nhóm. PASS khi registry tìm thấy tool, arguments hợp lệ, `error` là `None`, và kết quả đúng contract. Với action tool, chỉ dùng dry-run/`confirmed=False` cho quicktest.

## 5. `[CORE]` Tavily — `lookup`

- [API key](https://app.tavily.com)
- [Documentation](https://docs.tavily.com)

Thêm vào `.env`:

```bash
TAVILY_API_KEY=tvly-...
```

Smoke test:

```bash
python -c "from pathlib import Path; from env_loader import load_lab_env; load_lab_env(Path.cwd()); from tools import TOOL_FUNCTIONS as T; r=T['lookup']('AI', max_results=1); items=r.get('items') or []; print({'error':r.get('error'), 'message':r.get('message'), 'item_count':len(items), 'first_title':items[0].get('title') if items else None})"
```

## 6. `[CORE]` Firecrawl — `fetch`

- [Pricing](https://www.firecrawl.dev/pricing)
- [Documentation](https://docs.firecrawl.dev)

Thêm vào `.env`:

```bash
FIRECRAWL_API_KEY=fc-...
```

Smoke test:

```bash
python -c "from pathlib import Path; from env_loader import load_lab_env; load_lab_env(Path.cwd()); from tools import TOOL_FUNCTIONS as T; r=T['fetch']('https://example.com'); items=r.get('items') or []; print({'error':r.get('error'), 'message':r.get('message'), 'item_count':len(items), 'first_title':items[0].get('title') if items else None})"
```

## 7. `[CORE]` RapidAPI Twitter API45 — `timeline`, `social_search`

- [API page](https://rapidapi.com/alexanderxbx/api/twitter-api45)

Đăng ký plan của API, copy key, rồi thêm vào `.env`:

```bash
RAPIDAPI_KEY=...
RAPIDAPI_TWITTER_HOST=twitter-api45.p.rapidapi.com
```

Smoke tests:

```bash
python -c "from pathlib import Path; from env_loader import load_lab_env; load_lab_env(Path.cwd()); from tools import TOOL_FUNCTIONS as T; r=T['timeline']('sama', limit=1); items=r.get('items') or []; print({'error':r.get('error'), 'message':r.get('message'), 'item_count':len(items), 'first_title':items[0].get('title') if items else None})"
python -c "from pathlib import Path; from env_loader import load_lab_env; load_lab_env(Path.cwd()); from tools import TOOL_FUNCTIONS as T; r=T['social_search']('OpenAI', limit=1); items=r.get('items') or []; print({'error':r.get('error'), 'message':r.get('message'), 'item_count':len(items), 'first_title':items[0].get('title') if items else None})"
```

## 8. `[OPTIONAL]` arXiv/PDF — `papers`, `paper_text`

Không cần API key. arXiv có rate limit; tránh chạy liên tục.
Chỉ cần cài `pypdf` nếu nhóm chọn dùng `paper_text`.

Có thể đặt user agent của nhóm trong `.env`:

```bash
ARXIV_USER_AGENT="AI20k-Day04-Research-Agent/1.0 (your-team-name)"
```

Smoke tests:

```bash
python -c "from pathlib import Path; from env_loader import load_lab_env; load_lab_env(Path.cwd()); from tools import TOOL_FUNCTIONS as T; r=T['papers']('AI agent evaluation', max_results=1); items=r.get('items') or []; print({'error':r.get('error'), 'message':r.get('message'), 'item_count':len(items), 'first_title':items[0].get('title') if items else None})"
python -c "from pathlib import Path; from env_loader import load_lab_env; load_lab_env(Path.cwd()); from tools import TOOL_FUNCTIONS as T; r=T['paper_text']('1706.03762', max_pages=1); print({'error':r.get('error'), 'message':r.get('message'), 'chars_returned':r.get('chars_returned')})"
```

PDF tải về nằm trong `starter_v0/arxiv_papers/` và đã được gitignore.
Nếu `paper_text` báo `Install pypdf first`, chạy lại `python -m pip install -r requirements.txt`. Lỗi này không chặn core nếu team không dùng `paper_text`.

## 9. `[OPTIONAL]` Telegram live-send — `send`

1. Tạo bot bằng [@BotFather](https://t.me/BotFather).
2. Tạo private demo channel, thêm bot làm admin và chỉ cấp quyền cần thiết.
3. Dùng `@channel_username` hoặc chat ID do Telegram cung cấp.
4. Thêm vào `.env`:

```bash
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

Không đưa token vào command line, report, screenshot, transcript hoặc GitHub.

Smoke test mặc định chỉ kiểm tra confirmation boundary và không gửi message:

```bash
python -c "from pathlib import Path; from env_loader import load_lab_env; load_lab_env(Path.cwd()); from tools import TOOL_FUNCTIONS as T; r=T['send']('AI20k dry run', confirmed=False); print({'status':r.get('status'), 'error':r.get('error')})"
```

Chỉ test live-send vào private demo channel sau khi một người trong team xác nhận rõ. Không in raw exception vì URL lỗi của Telegram có thể chứa bot token.
Trong mọi `run_eval`, để Telegram credentials unset. Nếu chọn demo live-send, test thủ công ngoài eval.

## 10. UI và deploy/link cho team khác test

Streamlit được khuyến nghị vì dựng nhanh, nhưng nhóm có thể dùng bất kỳ framework nào hoặc nền tảng deploy nào.

### A. Chạy local

Nếu chọn Streamlit:

1. Chạy `python -m pip install "streamlit>=1.30.0"` và thêm `streamlit>=1.30.0` vào `requirements.txt`.
2. Tạo `app.py` trong `starter_v0/`.
3. Tái sử dụng `run_model_tool_loop` từ `chat.py` để UI và CLI dùng cùng agent loop; tiếp tục dùng cùng prompt/tool declarations với eval.
4. Hiển thị request/response, từng round với tool name + args + result/error, version/artifact, và lưu transcript. Không render/log secrets.
5. Chạy:

```bash
streamlit run app.py
```

PASS khi terminal không báo lỗi và mở được `http://localhost:8501`.

### B. Link tạm cho team khác test

`http://localhost:8501` chỉ đủ khi demo ngay trên máy trình chiếu. Nếu team khác cần mở từ máy khác, dùng deploy hoặc public tunnel. Ví dụ nhanh bằng Cloudflare Tunnel:

```bash
# macOS
brew install cloudflared

# Windows
winget install --id Cloudflare.cloudflared

# Sau khi UI đã chạy; thay port nếu framework dùng port khác
cloudflared tunnel --url http://localhost:8501
```

Linux xem [hướng dẫn cài cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

Link `trycloudflare.com` chỉ sống trong phiên tunnel, nên đây là link tạm chứ không phải deploy bền vững. Trước demo, kiểm tra lại link, quota và trace/log; sau demo tắt tunnel. Không nhập dữ liệu nhạy cảm vào UI public.

## Final checklist

### Core

- provider preflight chạy thành công;
- smoke-test thành công cho core APIs và tool mới bắt buộc;
- UI mở được và hiển thị request/response + tool trace + result/error;
- 3–5 kịch bản demo đã được rehearse;
- không có `.env`, API key hoặc token trong Git/report/log chia sẻ.

### Conditional / optional

- smoke-test optional built-ins chỉ khi nhóm dùng trong team eval hoặc demo;
- tool mới dùng để claim bonus phải có quicktest và evidence;
- nếu test live-send thì dùng private demo channel và giữ Telegram creds ngoài eval;
