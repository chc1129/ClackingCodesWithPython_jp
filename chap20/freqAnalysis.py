# 頻度分析プログラム
# https://www.nostarch.com/crackingcodes (BSD Licensed)

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def getLetterCount(message):
    # パラメータmessageに含まれている
    # 各文字の出現回数を保持する辞書を返す
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1

    return letterCount


def getItemAtIndexZero(items):
    return items[0]


def getFrequencyOrder(message):
    # パラメータmessageに含まれる
    # 文字の頻度順(降順)の文字列を返す

    # 最初に、各文字と出現回数のペアを保持する辞書を取得する
    letterToFreq = getLetterCount(message)

    # 第2に
    # 文字ごとの出現回数を辞書に登録する.
    freqToLetter = {}
    for letter in LETTERS:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)

    # 第3に、リストの文字を"ETAOIN"の逆順に配置し、
    # そのリストを文字列に変換する.
    for freq in freqToLetter:
        freqToLetter[freq].sort(key=ETAOIN.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    # 第4に、辞書freqToLetterをタプル(キーと値のペア)のリストに変換し、
    # それをソートする.
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=getItemAtIndexZero, reverse=True)

    # 第5に、文字は頻度淳に並べられ、
    # 文字全体を最終的な文字列として取り出す.
    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)


def englishFreqMatchScore(message):
    # パラメータmessageに含まれる文字列の頻度と
    # 英語の文字頻度を比較して、
    # マッチ数を返す.
    # ただし、マッチ数は、両者の文字頻度において、
    # 高頻度の6文字と低頻度の6文字で共通する文字数とする.
    freqOrder = getFrequencyOrder(message)

    matchScore = 0
    # 高頻度の6文字と共通する文字数をカウントする.
    for commonLetter in ETAOIN[:6]:
        if commonLetter in freqOrder[:6]:
            matchScore += 1
    # 低頻度の6文字と共通する文字数をカウントする.
    for uncommonLetter in ETAOIN[-6:]:
        if uncommonLetter in freqOrder[-6:]:
            matchScore += 1

    return matchScore
