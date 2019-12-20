from decouple import config
import requests

token = config("TELEGRAM_BOT_TOKEN")
url = "https://api.telegram.org/bot"
ngrok_url = "https://f73fe60c.ngrok.io"
paw_url = "https://yongnimm.pythonanywhere.com"

data = requests.get(f'{url}{token}/setWebhook?url={ngrok_url}/{token}')
# data = requests.get(f'{url}{token}/setWebhook?url={paw_url}/{token}')
print(data)