import requests
import urllib.parse
from datetime import datetime

def get_weather(location: str = "", date: str = "") -> dict:
    """Lấy thông tin thời tiết sử dụng wttr.in hoặc Open-Meteo cho dữ liệu lịch sử."""
    try:
        if date:
            # Parse date to check format (YYYY-MM-DD)
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d").date()
                today = datetime.now().date()
            except ValueError:
                return {"error": "Định dạng ngày không hợp lệ. Vui lòng dùng YYYY-MM-DD.", "weather": ""}

            if target_date < today:
                # Use Open-Meteo Geocoding
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(location)}&count=1&format=json"
                geo_resp = requests.get(geo_url, timeout=10)
                geo_resp.raise_for_status()
                geo_data = geo_resp.json()
                
                if not geo_data.get("results"):
                    return {"error": f"Không tìm thấy tọa độ cho địa điểm: {location}", "weather": ""}
                    
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
                
                # Use Open-Meteo Archive API
                archive_url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date}&end_date={date}&daily=temperature_2m_max,temperature_2m_min,rain_sum&timezone=auto"
                archive_resp = requests.get(archive_url, timeout=10)
                archive_resp.raise_for_status()
                archive_data = archive_resp.json()
                
                if "daily" in archive_data:
                    t_max = archive_data["daily"]["temperature_2m_max"][0]
                    t_min = archive_data["daily"]["temperature_2m_min"][0]
                    rain = archive_data["daily"]["rain_sum"][0]
                    return {
                        "error": None,
                        "weather": f"{location} (Ngày {date}): Nhiệt độ {t_min}°C - {t_max}°C. Lượng mưa: {rain}mm."
                    }
                else:
                    return {"error": f"Không có dữ liệu lịch sử cho {date}", "weather": ""}
        
        # Default to current weather via wttr.in
        loc_param = urllib.parse.quote(location) if location else ""
        url = f"https://wttr.in/{loc_param}?format=3"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        return {
            "error": None,
            "weather": response.text.strip()
        }
    except Exception as e:
        return {
            "error": f"Lỗi truy xuất thời tiết: {str(e)}",
            "weather": ""
        }
