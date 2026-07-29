# weather_forecast

## Mục đích
Lấy thông tin thời tiết hiện tại sử dụng API wttr.in, hoặc thông tin thời tiết trong quá khứ (Historical Weather) sử dụng Open-Meteo Archive API.

## Khi nào dùng
- Khi người dùng hỏi "Thời tiết ở X hôm nay thế nào?" (Dùng wttr.in)
- Khi người dùng hỏi "Thời tiết ở X ngày hôm qua ra sao?" hoặc các ngày trong quá khứ (Dùng Open-Meteo Archive API kết hợp Geocoding).

## Lưu ý
- Địa điểm có thể là tên thành phố, hoặc để trống (lấy IP hiện tại).
- Nếu tra cứu trong quá khứ, Agent phải cung cấp thêm tham số `date` theo định dạng `YYYY-MM-DD`.
