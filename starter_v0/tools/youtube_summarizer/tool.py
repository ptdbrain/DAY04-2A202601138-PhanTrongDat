try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

def get_youtube_transcript(url: str, max_chars: int = 15000) -> dict:
    """Lấy transcript của video Youtube."""
    if YouTubeTranscriptApi is None:
        return {"error": "Thiếu thư viện youtube-transcript-api. Vui lòng chạy `pip install youtube-transcript-api`", "text": ""}
    try:
        # Extract Video ID from URL
        parsed = urllib.parse.urlparse(url)
        video_id = ""
        
        if parsed.hostname in ('youtu.be', 'www.youtu.be'):
            video_id = parsed.path[1:]
        elif parsed.hostname in ('youtube.com', 'www.youtube.com'):
            if parsed.path == '/watch':
                query = urllib.parse.parse_qs(parsed.query)
                video_id = query.get('v', [''])[0]
            elif parsed.path.startswith(('/embed/', '/v/')):
                video_id = parsed.path.split('/')[2]
        
        if not video_id:
            # Fallback assuming the user passed raw ID
            video_id = url
            
        # Get transcript (try vi then en)
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=['vi', 'en'])
        
        # Combine text
        full_text = " ".join([t.text for t in transcript])
        
        # Truncate to avoid context window explosion
        if len(full_text) > max_chars:
            full_text = full_text[:max_chars] + "...\n[Đã bị cắt ngắn do độ dài]"
            
        return {
            "error": None,
            "text": full_text
        }
    except Exception as e:
        return {
            "error": f"Không thể lấy transcript từ Youtube: {str(e)}",
            "text": ""
        }
