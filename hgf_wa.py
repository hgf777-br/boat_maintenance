from pywa import WhatsApp
from pywa.types import Template as Temp

wa = WhatsApp(
    phone_id="608083275721320",
    token="EAAJALjDhCW4BO4loly9QXPY9USKoAALo09fRhtB0MTQh4mGFw930eYvBiEDHYtEEyNZCTX5nrRnLKla7ZBgbPHKoNzKkvG8b2Gu7we9bXYphZBHRRvZArFwxjDn1o4zA1DjI8Mhskyft4Wu5hlzPecOFsyCqaOmf3xLB9XJBDzp6jjX7n1QNUEKI2HZAusIehXvD1qTvZApECVnuDJ8ZAc9JbTNQP70etQ23OVSridj"
)

# Send a template message
wa.send_template(
    to="5511992966121",
    template=Temp(
        name="hello_world",
        language=Temp.Language.ENGLISH_US,
    )
)
