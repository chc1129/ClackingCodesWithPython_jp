# 英語検知モジュール
# https://www.nostarch.com/crackingcodes/ (BSD License)

# 使用するには次のコードを入力する.
#   import detectEnglish
#   detectingEnglish.isEnglish(someString) # TrueまたはFalseを返す
# このプログラムがあるディレクトリ内には"dictionary.txt"ファイルがなければならない.
# 辞書ファイルには1行ごとに1つの英単語が記述されているものとする.
# https://inventwithpython.com/dictionary.txtからダウンロードできる.
UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACE = UPPERLETTERS + UPPERLETTERS.lower() + ' \t\n'

def loadDictionary():
    dictionaryFile = open('dictionary.txt')
    englishwords = {}
    for word in dictionaryFile.read().split('\n'):
        englishwords[word] = None
    dictionaryFile.close()
    return englishwords

ENGLISH_WORDS = loadDictionary()


def getEnglishCount(message):
    message = message.upper()
    message = removeNonLetters(message)
    possibleWords = message.split()

    if possibleWords == []:
        return 0.0 # 単語がなければ, 0.0を返す.

    matches = 0
    for word in possibleWords:
        if word in ENGLISH_WORDS:
            matches += 1
    return float(matches) / len(possibleWords)


def removeNonLetters(message):
    lettersOnly = []
    for symbol in message:
        if symbol in LETTERS_AND_SPACE:
            lettersOnly.append(symbol)
    return ''.join(lettersOnly)


def isEnglish(message, wordPercentage=20, letterPercentage=85):
    # デフォルトでは, 単語の20%が辞書ファイルに存在していなければならない.
    # メッセージの85%は, 句読点や数字を除く文字,
    # あるいは空白でなければならない.
    wordsMatch = getEnglishCount(message) * 100 >= wordPercentage
    numLetters = len(removeNonLetters(message))
    messageLettersPercentage = float(numLetters) / len(message) * 100
    lettersMatch = messageLettersPercentage >= letterPercentage
    return wordsMatch and lettersMatch
