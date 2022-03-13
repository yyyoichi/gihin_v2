from request.Minute import Minute
from request.Url import Url


maker  = Url(3)
maker.any("コロナ")
maker.recordPacking("json")
maker.from_("2021-01-01")
maker.until("2022-03-10")
url = maker.getUrl()
print(url)
fetch = Minute(url)
r = fetch.get()
if r == None:
    exit()
print(r.numberOfReturn())
it = r.iterator()
if it.has_next():
    rc = it.next()
    print(rc.speaker())
    print(rc.speakerYomi())
    print(rc.speech())

