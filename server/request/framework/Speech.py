
import re
import neologdn


class Speech:
    def __init__(self, text) -> None:
        self.t = self.__preprocessing(text)

    def __preprocessing(self, text: str) -> str:
        text = re.sub(r"○.*　", "", text)
        text = re.sub(r'\n', '', text)
        text = re.sub(r'\r', '', text)
        text = re.sub(r'\s', '', text)
        text = neologdn.normalize(text)
        text = text.lower()
        return text

    def text(self):
        return self.t
    
    def getSentences(self):
        sentences = [s+"。" for s in self.t.split('。') if s]
        return sentences