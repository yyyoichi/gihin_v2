from collections import Counter
import itertools
from request.Minute import Minute
from request.Url import Url
from language.Token import Morpheme


KEYWORD = "コロナ"
DAY = "2022-06-23"
stop_words = ["君", "*", "等", "こと", "ため", "これ", "の", "この", "あの", "よう", "ふう", "もの", "ところ", "それ", "ん", "わけ", "とき", "回", "目"]
#形態素解析器
m = Morpheme()
#url作成
maker  = Url(3)
maker.any(KEYWORD)
maker.maximumRecords("50")#50コ取得
maker.nameOfHouse("参議院")
maker.searchRange("本文")
maker.recordPacking("json")
# maker.from_("2021-01-01")
maker.until(DAY)
url = maker.getUrl()#設定したクエリをもつURLを取得する
print(url)
#議事録データを取得
#コロナにヒットする発言データが帰ってくる
res = Minute(url).get()
if res == None:
    exit()
doublets = []
it = res.iterator()#発言をループする
while it.has_next():
    rc = it.next()#発言のデータ
    # print(rc.speaker())
    # print(rc.speakerYomi())
    speech = rc.speech()
    sentences = speech.getSentences()#　。（読点）区切りでリスト化
    
    for sentence in sentences:
        if KEYWORD not in sentence:
            #コロナというワードがなければスルー
            continue
        #形態素解析された原形の単語をもつリスト, 名詞のみとりだし
        print(sentence)
        words = [w.prototype() for w in m.parse(sentence).getValues() if w.part_of_speech()== "名詞" and w.surface() not in stop_words and w.part_of_speech_details_1() != "数"]
        # 共起のペアをリストで取得
        dls = list(itertools.combinations(words, 2))
        doublets.extend(dls)
            
dic = Counter(doublets)#出現回数をカウント
dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)[:50]#上位50位を取得
print("\n")
print("結果\n"+"キーワード: "+KEYWORD+", 日時終点: "+DAY)
for d in dic:
    print(d)
    

