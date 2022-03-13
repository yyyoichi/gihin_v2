import urllib.parse


class Url:
    """
    国会会議録検索システム（ウェブサイト）での検索と同等の検索、返戻機能を有しています。
    HTTPのGetメソッドで送信された検索リクエストに対し、XML形式又はJSON形式でデータを返戻します。
    次の3種類の検索APIがあります。検索リクエストの指定方法は同じですが、データの返戻形式が異なります。
    """

    query = []
    def __init__(self, number: int) -> None:
        """(1) 会議単位簡易出力では、指定した検索条件でヒットした会議録の情報（回次、院、会議名、号、開催日、ID、URL等）を、1リクエストに対し最大100件まで、XML形式又はJSON形式で返戻します。
    アクセスURLは https://kokkai.ndl.go.jp/api/meeting_list?{検索条件} です。
    発言を対象に検索した場合には、会議録中の該当する発言の情報（発言者名、発言順、ID、URL）も合わせて返戻します。
    本文のテキストデータは返戻しません。\n
    (2) 会議単位出力では、指定した検索条件でヒットした会議録の情報（回次、院、会議名、号、開催日、ID、URL等）と、当該会議録の全ての発言本文のテキストデータ（発言者等の情報を含みます。）を、1リクエストに対し最大10件まで、XML形式又はJSON形式で返戻します。
    アクセスURLは https://kokkai.ndl.go.jp/api/meeting?{検索条件} です。
    本文のテキストデータが返戻される点で(1) 会議単位簡易出力と、会議録中の全ての発言が返戻される点で(3) 発言単位出力と異なります。\n
    (3) 発言単位出力では、指定した検索条件でヒットした発言本文のテキストデータ（発言者の情報を含みます。）を、その発言が含まれる会議録の情報（回次、院、会議名、号、開催日、ID、URL等）と共に、1リクエストに対し最大100件まで、XML形式又はJSON形式で返戻します。
    アクセスURLは https://kokkai.ndl.go.jp/api/speech?{検索条件} です。
    本文のテキストデータが返戻される点で(1) 会議単位簡易出力と、ヒットした発言だけが返戻される点で(2) 会議単位出力と異なります。\n\n
    検索結果のソート順は、会議開催日の新しい順となっています。
        Args: 
            number (int): リクエストタイプ
        """
        if number == 1:
            self.url = "https://kokkai.ndl.go.jp/api/meeting_list?"
        elif number == 2:
            self.url = "https://kokkai.ndl.go.jp/api/meeting?"
        elif number == 3:
            self.url = "https://kokkai.ndl.go.jp/api/speech?"
        else:
            print("number requre 1, 2, 3")

    def getUrl(self):
        return self.url + "&".join(self.query)

    def startRecord(self, value: str):
        """検索結果の取得開始位置を「1～検索件数」の範囲で指定可能。
        省略時のデフォルト値は「1」
        Args: 
            value (str): 開始位置
        """
        q = self.__getQuery("startRecord", value)
        self.__addQuery(q)

    def maximumRecords(self, value: str):
        """一回のリクエストで取得できるレコード数を、会議単位簡易出力、発言単位出力の場合は「1～100」、会議単位出力の場合は「1～10」の範囲で指定可能。
    省略時のデフォルト値は、会議単位簡易出力、発言単位出力の場合は「30」、会議単位出力の場合は「3」
        Args: 
            value (str): 一回の最大取得件数
        """
        q = self.__getQuery("maximumRecords", value)
        self.__addQuery(q)

    def nameOfHouse(self, value: str):
        """院名として「衆議院」「参議院」「両院」「両院協議会」のいずれかを指定可能。「両院」と「両院協議会」の結果は同じ。
    省略可（省略時は検索条件に含めない）。また、指定可能な値以外を指定した場合も、検索条件に含めない。
        Args: 
            value (str): 院名
        """
        q = self.__getQuery("nameOfHouse", value)
        self.__addQuery(q)

    def nameOfMeeting(self, value: str):
        """本会議、委員会等の会議名（ひらがな可）を指定可能。部分一致検索。半角スペース（U+0020）を区切り文字として複数指定した場合は、指定した語のOR検索となる。
    省略可（省略時は検索条件に含めない）。
        Args: 
            value (str): 会議名
        """
        q = self.__getQuery("nameOfMeeting", value)
        self.__addQuery(q)

    def any(self, value: str):
        """発言内容等に含まれる言葉を指定可能。部分一致検索。半角スペース（U+0020）を区切り文字として複数指定した場合は、指定した語のAND検索となる。
    省略可（省略時は検索条件に含めない）。
        Args: 
            value (str): 検索語
        """
        q = self.__getQuery("any", value)
        self.__addQuery(q)

    def from_(self, value: str):
        """検索対象とする会議の開催日の始点を「YYYY-MM-DD」の形式で指定可能。
    省略可（省略時は「0000-01-01」が指定されたものとして検索する）。
        Args: 
            value (str): 開会日付／始点
        """
        q = self.__getQuery("from", value)
        self.__addQuery(q)

    def until(self, value: str):
        """検索対象とする会議の開催日の終点を「YYYY-MM-DD」の形式で指定可能。
    省略可（省略時は「9999-12-31」が指定されたものとして検索する）。
        Args: 
            value (str): 開会日付／終点
        """
        q = self.__getQuery("until", value)
        self.__addQuery(q)

    def supplementAndAppendix(self, value: str):
        """検索対象を追録・附録に限定するか否かを「true」「false」で指定可能。
    省略可（省略時は「false」（限定しない）が指定されたものとして検索する）。
        Args: 
            value (str): 追録・附録指定
        """
        q = self.__getQuery("supplementAndAppendix", value)
        self.__addQuery(q)

    def contentsAndIndex(self, value: str):
        """検索対象を目次・索引に限定するか否かを「true」「false」で指定可能。
    省略可（省略時は「false」（限定しない）が指定されたものとして検索する）。
        Args: 
            value (str): 目次・索引指定
        """
        q = self.__getQuery("contentsAndIndex", value)
        self.__addQuery(q)

    def searchRange(self, value: str):
        """検索語（パラメータ名：any）を指定して検索する際の検索対象箇所を「冒頭」「本文」「冒頭・本文」のいずれかで指定可能。
    省略可（省略時は「冒頭・本文」が指定されたものとして検索する）。検索語を指定しなかった時は検索条件には含めない。
        Args: 
            value (str): 議事冒頭・本文指定
        """
        q = self.__getQuery("searchRange", value)
        self.__addQuery(q)

    def closing(self, value: str):
        """検索対象を閉会中の会議録に限定するか否かを「true」「false」で指定可能。
    省略可（省略時は「false」（限定しない）が指定されたものとして検索する）。
        Args: 
            value (str): 閉会中指定
        """
        q = self.__getQuery("closing", value)
        self.__addQuery(q)

    def speechNumber(self, value: str):
        """発言番号を0以上の整数（例：発言番号10の場合は「speechNumber=10」）で指定可能。完全一致検索。
    省略可（省略時は検索条件に含めない）。
        Args: 
            value (str): 発言番号
        """
        q = self.__getQuery("speechNumber", value)
        self.__addQuery(q)

    def speakerPosition(self, value: str):
        """発言者の肩書きを指定可能。部分一致検索。
    省略可（省略時は検索条件に含めない）。
        Args: 
            value (str): 発言者肩書き
        """
        q = self.__getQuery("speakerPosition", value)
        self.__addQuery(q)

    def speakerGroup(self, value: str):
        """発言者の所属会派を指定可能。部分一致検索（なお、登録されているデータは正式名称のみ）。
    省略可（省略時は検索条件に含めない）。
        Args: 
            value (str): 発言者所属会派
        """
        q = self.__getQuery("speakerGroup", value)
        self.__addQuery(q)

    def speakerRole(self, value: str):
        """発言者の役割として「証人」「参考人」「公述人」のいずれかを指定可能。
    省略可（省略時は検索条件に含めない）。指定可能な値以外を指定した場合はエラーになる。
        Args: 
            value (str): 発言者役割
        """
        q = self.__getQuery("speakerRole", value)
        self.__addQuery(q)

    def speechID(self, value: str):
        """発言を一意に識別するIDとして、「会議録ID（パラメータ名：issueID。21桁の英数字）_発言番号（会議録テキスト表示画面で表示されている各発言に付されている、先頭に0を埋めて3桁にした数字。4桁の場合は4桁の数字）」の書式で指定可能（例：「100105254X00119470520_000」）。完全一致検索。
    省略可（省略時は検索条件に含めない）。書式が適切でない場合にはエラーになる。
        Args: 
            value (str): 発言ID
        """
        q = self.__getQuery("speechID", value)
        self.__addQuery(q)

    def issueID(self, value: str):
        """会議録（冊子）を一意に識別するIDとして、会議録テキスト表示画面の「会議録テキストURLを表示」リンクで表示される21桁の英数字で指定可能（例：「100105254X00119470520」）。完全一致検索。
    省略可（省略時は検索条件に含めない）。書式が適切でない場合にはエラーになる。
        Args: 
            value (str): 会議録ID
        """
        q = self.__getQuery("issueID", value)
        self.__addQuery(q)

    def sessionFrom(self, value: str):
        """検索対象とする国会回次の始まり（開始回）を3桁までの自然数で指定可能。国会回次Toと組み合わせて指定した場合には範囲指定検索、国会回次From単独で指定した場合は当該の回次のみを完全一致検索。
    省略可（省略時は検索条件に含めない）。
        Args: 
            value (str): 国会回次From
        """
        q = self.__getQuery("sessionFrom", value)
        self.__addQuery(q)

    def sessionTo(self, value: str):
        """検索対象とする国会回次の終わり（終了回）を3桁までの自然数で指定可能。国会回次Fromと組み合わせて指定した場合には範囲指定検索、国会回次To単独で指定した場合は当該の回次のみを完全一致検索。
    省略可（省略時は検索条件に含めない）。
        Args: 
            value (str): 国会回次To
        """
        q = self.__getQuery("sessionTo", value)
        self.__addQuery(q)

    def issueFrom(self, value: str):
        """検索対象とする号数の始まり（開始号）を3桁までの整数で指定可能（目次・索引・附録・追録は0号扱い）。号数Toと組み合わせて指定した場合には範囲指定検索、号数From単独で指定した場合は当該の回次のみを完全一致検索。
    省略可（省略時は検索条件に含めない）。
        Args: 
            value (str): 号数From
        """
        q = self.__getQuery("issueFrom", value)
        self.__addQuery(q)

    def issueTo(self, value: str):
        """検索対象とする号数の終わり（終了号）を3桁までの整数で指定可能（目次・索引・附録・追録は0号扱い）。号数Fromと組み合わせて指定した場合には範囲指定検索、号数To単独で指定した場合は当該の回次のみを完全一致検索。
    省略可（省略時は検索条件に含めない）。
        Args: 
            value (str): 号数To
        """
        q = self.__getQuery("issueTo", value)
        self.__addQuery(q)

    def recordPacking(self, value: str):
        """検索リクエストに対する応答ファイルの形式として、「xml」「json」のいずれかを指定可能。
    省略可（省略時は「xml」が指定されたものとして検索する）。
        Args: 
            value (str): 応答形式
        """
        q = self.__getQuery("recordPacking", value)
        self.__addQuery(q)

    def __encode(self, value: str) -> str:
        return urllib.parse.quote(value)

    def __getQuery(self, param: str, value: str):
        return param + "=" + self.__encode(value)

    def __addQuery(self, query: str):
        self.query.append(query)
