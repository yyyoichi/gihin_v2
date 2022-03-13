import requests

from request.framework.Recode import Recode

class Minute:
    def __init__(self, url) -> None:
        self.url = url

    def get(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            print("success")
            json = res.json()
            return Recode(json)
        else:
            print("failuter")
