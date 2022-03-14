class Word:
    def __init__(self, line) -> None:
        l = line.split("\t")
        self.s = l[0]
        self.data = l[1].split(",")
    
    def surface(self) -> str:
        """
        表層形
        """
        return self.s

    def part_of_speech(self) -> str:
        """
        品詞
        """
        return self.data[0]

    def part_of_speech_details_1(self) -> str:
        """
        品詞細分類1
        """
        return self.data[1]

    def part_of_speech_details_2(self) -> str:
        """
        品詞細分類2
        """
        return self.data[2]

    def part_of_speech_details_3(self) -> str:
        """
        品詞細分類3
        """
        return self.data[3]

    def inflection(self) -> str:
        """
        活用型
        (一段など)
        """
        return self.data[4]
    
    def inflected_form(self) -> str:
        """
        活用形
        (基本形など)
        """
        return self.data[5]

    
    def prototype(self) -> str:
        """
        原形
        """
        return self.data[6]

    def reading(self) -> str:
        """
        読み
        """
        return self.data[7]

    def pronunciation(self) -> str:
        """
        発音
        """
        return self.data[8]
    