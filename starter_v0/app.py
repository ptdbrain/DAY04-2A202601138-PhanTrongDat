from pathlib import Path
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from chat import run_model_tool_loop, trim_history, ARTIFACTS_DIR, ROOT, write_transcript, build_artifact_version
import time
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# Mount static folder
static_dir = ROOT / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialization logic
load_lab_env(ROOT)
system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
tools_yaml_path = ARTIFACTS_DIR / "tools.yaml"

provider = make_provider("openrouter")
model = getattr(provider, "default_model", None)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_file = static_dir / "index.html"
    if not index_file.exists():
        return "<h1>UI is building...</h1>"
    return index_file.read_text(encoding="utf-8")

@app.post("/api/chat")
async def api_chat(request: Request):
    data = await request.json()
    user_text = data.get("user_text", "")
    history = data.get("history", []) 
    
    # Reload prompt/tools on every request for hot-reloading in lab
    sys_prompt = system_prompt_path.read_text(encoding="utf-8")
    
    # Inject current datetime so the agent can resolve relative dates (e.g. 'hôm qua')
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sys_prompt += f"\n\n[SYSTEM INFO]\nHôm nay là ngày: {current_time_str}"
    
    t_decls = load_tool_declarations(tools_yaml_path)
    o_tools = to_openai_tools(t_decls)
    
    messages = [
        {"role": "system", "content": sys_prompt},
        *trim_history(history, 5),
        {"role": "user", "content": user_text},
    ]
    
    from openai import APIStatusError
    try:
        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=o_tools,
            model=model,
            max_tool_rounds=4,
        )
    except APIStatusError as e:
        error_message = e.response.json().get('error', {}).get('message', str(e))
        return {
            "status": "error",
            "assistant_text": f"🚨 **Lỗi API (Hết tiền hoặc Giới hạn):** {error_message}",
            "rounds": [],
            "tool_events": []
        }
    except Exception as e:
        return {
            "status": "error",
            "assistant_text": f"🚨 **Lỗi Hệ thống Không xác định:** {str(e)}",
            "rounds": [],
            "tool_events": []
        }
        
    art_ver_obj = build_artifact_version("v3", system_prompt_path, tools_yaml_path)
    art_ver = art_ver_obj.artifact_version
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_path = ROOT / "transcripts" / f"{art_ver.split('+')[0]}_openrouter_{timestamp}.transcript.json"
    
    transcript = {
        "artifact_version": art_ver,
        "history": history + [
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": result.get("assistant_text")}
        ],
        "tool_events": result.get("tool_events", [])
    }
    
    transcript_path.parent.mkdir(exist_ok=True)
    write_transcript(transcript_path, transcript)
    
    result["artifact_version"] = art_ver
    result["transcript_path"] = str(transcript_path.relative_to(ROOT))
    
    return result
