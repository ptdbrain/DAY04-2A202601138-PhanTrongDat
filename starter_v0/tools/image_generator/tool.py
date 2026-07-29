import urllib.parse

def generate_image(prompt: str) -> dict:
    """Tạo URL ảnh từ pollinations.ai dựa trên text prompt."""
    try:
        # pollinations.ai accepts simple GET requests with prompt in path
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=400&nologo=true"
        
        return {
            "error": None,
            "image_url": image_url,
            "markdown_code": f"![{prompt}]({image_url})"
        }
    except Exception as e:
        return {
            "error": f"Lỗi tạo ảnh: {str(e)}",
            "image_url": ""
        }
