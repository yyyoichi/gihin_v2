

from request.framework.SpeechRecode import SpeechRecode


class Recode:
    def __init__(self, response) -> None:
        self.response = response

    def numberOfRecords(self) -> str:
        """
        Returns:
            str: 総結果件数
        """
        return self.response["numberOfRecords"]

    def numberOfReturn(self) -> str:
        """
        Returns:
            str: 返戻件数
        """
        return self.response["numberOfReturn"]

    def nextRecordPosition(self) -> str:
        """
        Returns:
            str: 次開始位置
        """
        return self.response["nextRecordPosition"]

    def speechRecord(self):
        """
        Returns:
            list: 発言情報
        """
        return self.response["speechRecord"]

    def speechRecordAt(self, index: int):
        """
        Returns:
            SpeechRecode: 発言情報
        """
        r = self.response["speechRecord"][index]
        return SpeechRecode(r)

    def iterator(self):
        return RecodeIterator(self)


class RecodeIterator:
    index = 0
    def __init__(self, Recode: Recode) -> None:
        self.Recode = Recode
    
    def has_next(self):
        if self.index < self.Recode.numberOfReturn():
            return True
        else:
            return False
    
    def next(self):
        sr = self.Recode.speechRecordAt(self.index)
        self.index += 1
        return sr
    
