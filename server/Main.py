from collections import Counter
from request.Minute import Minute
from request.Url import Url
from language.Token import Morpheme

KEYWORD = "コロナ"
#形態素解析器
m = Morpheme()
#url作成
maker  = Url(3)
maker.any(KEYWORD)
maker.maximumRecords("30")#30コ取得
maker.nameOfHouse("参議院")
maker.recordPacking("json")
# maker.from_("2021-01-01")
maker.until("2020-03-14")
url = maker.getUrl()#設定したクエリをもつURLを取得する
print(url)
#議事録データを取得
fetch = Minute(url)
#コロナにヒットする発言データが帰ってくる
res = fetch.get()
if res == None:
    exit()
n_gram = []
it = res.iterator()#発言をループする
while it.has_next():
    rc = it.next()#発言のデータ
    print(rc.speaker())
    print(rc.speakerYomi())
    speech = rc.speech()
    sentences = speech.getSentences()#　。（読点）区切りでリスト化
    
    for sentence in sentences:
        if KEYWORD not in sentence:
            #コロナというワードがなければスルー
            continue
        #形態素解析された原形の単語をもつリスト
        words = [w.prototype() for w in m.parse(sentence).getValues()]
        d = list(zip(words[:-1], words[1:]))#2つセットにする
        n_gram.extend(d)
dic2 = Counter(n_gram)#出現回数をカウント
dic2 = sorted(dic2.items(), key=lambda x: x[1], reverse=True)[:50]#上位50位を取得
print("\n")
print("結果")
for d in dic2:
    print(d)
    

