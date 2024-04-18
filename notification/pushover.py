import requests

url = "https://api.pushover.net/1/messages.json"
def send_pushover_notification(key,token,message):
    r = requests.post(url, data={
    'user': key,
    'token': token,
    'message': message,
})
    if r.status_code != 200:
        print('Failed to send Pushover notification.')
    

