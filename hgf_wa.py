from pywa import WhatsApp
from pywa.types import Template as Temp

wa = WhatsApp(
    phone_id="608083275721320",
    token="EAAJALjDhCW4BOZCTnBTiu04VPccZAGY8IyDbGT5H0bzgB2lTpjtTCZCh3tbiBBs3LHR3vKJIEnBC2TwzSBhhULk4fkZBVbpXa3OxPzR2ZCVf8ABa6rfHZClfbsynJJarSa1kUSgYnfaqHc7wRvy5mLGr8FDOkpe3ZAhcp5kYyZCJDZB8YQQi1ZCV78PhtiGtkyQAq6cBMQZAtijQhSXqGdbEvpLYcSDa9xs"
)

# Send a message
wa.send_message(to="5511958719095", text="Oi Bruna do Python! Estou testando a biblioteca pywa para WhatsApp.")

# Send a template message
# wa.send_template(
#     to="5511958719095",
#     template=Temp(
#         name="hello_world",
#         language=Temp.Language.ENGLISH_US,
#     )
# )
