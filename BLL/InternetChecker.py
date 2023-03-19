import urllib.request

class InternetChecker:
    def __init__(self) -> None:
        pass
    def check(self):
        try:
            urllib.request.urlopen('http://google.comx', timeout=1)
            return True
        except urllib.request.URLError:
            return False