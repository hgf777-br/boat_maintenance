import json
import requests
from requests.structures import CaseInsensitiveDict

url = "https://graph.facebook.com/v22.0/608083275721320/messages"

headers = CaseInsensitiveDict()
headers["Authorization"] = "Bearer EAAJALjDhCW4BO9MiaJLXSwgLSdDdYKdNDBvmsiGUlHZBuh0WHHZCaCattXSQ9Ql5sZBqOZBPrYW0COKhpgKKv6KYtCZAZC50rotJZA0BZCfW4nvZA2ZABGUAz11fuyZCEd4ons9rGiTukFcyeLTuOvajgLWib7ZAbjkRfKTfoijiXVu6r4D0a8oyokAr6tp7GF2Hvg45CaJDiFimb6OgYpcT1HniG1iiWUgZD"
headers["Content-Type"] = "application/json"
data = {
        "messaging_product": "whatsapp",
        "to": "5511992966121",
        "type": "template",
        "template": {
            "name":"maintenance_reminder",
            "language":{
                "code":"pt_BR"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "parameter_name": "maintenance",
                            "text": "consertar a tela"
                        },
                        {
                            "type": "text",
                            "parameter_name": "technician",
                            "text": "Fernando"
                        },
                    ]
                }
            ]
        }
    }

resp = requests.post(url, headers=headers, json=data)

print(resp.json())

