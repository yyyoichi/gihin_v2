from collections import Counter
from request.Minute import Minute
from request.Url import Url
from language.Token import Morpheme

KEYWORD = "コロナ"

m = Morpheme()
maker  = Url(3)
maker.any(KEYWORD)
maker.maximumRecords("30")
maker.nameOfHouse("参議院")
maker.recordPacking("json")
# maker.from_("2021-01-01")
# maker.until("2022-03-10")
url = maker.getUrl()
print(url)
fetch = Minute(url)
res = fetch.get()
if res == None:
    exit()
n_gram = []
it = res.iterator()
while it.has_next():
    rc = it.next()
    print(rc.speaker())
    print(rc.speakerYomi())
    speech = rc.speech()
    sentences = speech.getSentences()
    
    for sentence in sentences:
        if KEYWORD not in sentence:
            continue
        words = [w.prototype() for w in m.parse(sentence).getValues()]
        d = list(zip(words[:-1], words[1:]))
        n_gram.extend(d)
dic2 = Counter(n_gram)
dic2 = sorted(dic2.items(), key=lambda x: x[1], reverse=True)[:50]
print(dic2)
    

