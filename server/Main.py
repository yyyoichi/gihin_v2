from collections import Counter
import itertools
from request.Minute import Minute
from request.Url import Url
from language.Token import Morpheme
from igraph import *


KEYWORD = "電力"
DAY = "2022-06-23"
stop_words = ["中", '*', "君", "*", "等", "こと", "ため", "これ", "の", "この", "あの", "よう", "ふう", "もの", "ところ", "それ", "ん", "わけ", "とき", "回", "目"]
#形態素解析器
m = Morpheme()
#url作成
maker  = Url(3)
maker.any(KEYWORD)
maker.maximumRecords("50")#50コ取得
maker.nameOfHouse("参議院")
maker.searchRange("本文")
maker.recordPacking("json")
maker.until(DAY)
url = maker.getUrl()#設定したクエリをもつURLを取得する
print(url)
#議事録データを取得
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
            #keyワードがなければスルー
            continue
        words = [w.prototype() for w in m.parse(sentence).getValues() if w.part_of_speech()== "名詞" and w.surface() not in stop_words and w.part_of_speech_details_1() != "数" and w.prototype() != "*"]
        # 共起のペアをリストで取得
        dls = list(itertools.combinations(words, 2))
        doublets.extend(dls)
            
dic = Counter(doublets)#出現回数をカウント
print(sorted(dic.items(), key=lambda x: x[1], reverse=True)[:50])#上位50位を取得
restricteddcnt = dict( ( (k, dic[k]) for k in dic.keys() if dic[k] >= 4))
# ペア単語のタプル
charedges = restricteddcnt.keys()
# 出てきた単語リスト（set 済み）頂点となる
vertices = list(set( [v[0] for v in charedges] + [v[1] for v in charedges]))
# 共起ペアが、頂点と頂点を結ぶ。辺となる
edges = [(vertices.index(u[0]), vertices.index(u[1])) for u in charedges]
g = Graph(vertex_attrs={"label": vertices, "name":vertices}, edges=edges, directed=False)
plot(g, vertex_size=30, bbox=(800, 800), vertex_color='white')
    

