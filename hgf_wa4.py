from pywa import WhatsApp
from pywa.types import Template as Temp

wa = WhatsApp(
    phone_id="608083275721320",
    token="EAAJALjDhCW4BO36DYwARFJdYAjeNi7k0qpcpnD2ZAkd74ZAF6ZAzQGgA8p6tv1ZBcYogHSvRNiIZABVLv9rDFxpMMkI80vFtKVY9MEXdOQYspB39bZCn6tLuZCwL5Tg4MUhzqVEC8c5PpCfavQ3bw7ZAlXjM9OIM6eyUanqyPg56sWEeArsRH13OIiTrmZCvYnKV6HWiWKXhJxlbGS5IZBwT0XOIZBOZARtMHIvOTZCspARZAY"
)

# Send a template message
wa.send_template(
    to="+5511992966121",
    template=Temp(
        name="maintenance",
        language=Temp.Language.PORTUGUESE_BR,
        body=[
            Temp.TextValue(value='15/05/2025'),
            Temp.TextValue(value='Blue Note'),
            Temp.TextValue(value='Fernando'),
            Temp.TextValue(value='Troca do exaustor de popa'),
        ],
    )
)
