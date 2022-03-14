import MeCab

from language.Word import Word

class Morpheme:
    def __init__(self) -> None:
        self.t = MeCab.Tagger("C:\Program Files\MeCab\etc\mecabrc")
    def parse(self, text: str):
        p = self.t.parse(text)
        return Line(p)


class LineIterator:
    def __init__(self, lines):
        self.lines = lines
        self.index = 0
    
    def has_next(self):
        l = self.lines.getLength()-1
        if self.index < l:
            return True
        else:
            return False
    
    def next(self) -> Word:
        l = self.lines.getLineAt(self.index)
        self.index += 1
        return l

class Line:
    def __init__(self, corpas):
        self.corpas = corpas
        self.lines = corpas.split('\n')

    def getLineAt(self, index):
        return Word(self.lines[index]) 
    
    def getLength(self):
        return len(self.lines)-1
    
    def iterator(self):
        return LineIterator(self)
    
    def wakachi(self):
        it = self.iterator()
        wakachi = []
        while it.has_next():
            word = it.next()
            w = word.surface()
            wakachi.append(w)
        return " ".join(wakachi)


    def getValues(self) -> list[Word]:
        it = self.iterator()
        list = []
        while it.has_next():
            l = it.next()
            list.append(l)
        return list

