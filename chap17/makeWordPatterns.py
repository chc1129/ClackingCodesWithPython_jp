# wordPatterns.pyファイルを作成する
# https://www.nostarch.com/crackingcodes (BSD Licensed)

# 同一フォルダー内にある辞書ファイル（dictionary.txt）から
# 単語パターンと単語のペアを保持するwordPatterns.pyを作成する.
# 辞書ファイルはhttps://invpy.com/dictionary.txtからダウンロードできる.

import pprint


def getWordPattern(word):
    # 与えられた単語の単語パターンの文字列を返す.
    # 例：'DUSTBUSTER'なら'0.1.2.3.4.1.2.3.5.6'
    word = word.upper()
    nextNum = 0
    letterNums = {}
    wordPattern = []

    for letter in word:
        if letter not in letterNums:
            letterNums[letter] = str(nextNum)
            nextNum += 1
        wordPattern.append(letterNums[letter])
    return '.'.join(wordPattern)


def main():
    allPatterns = {}

    fo = open('dictionary.txt')
    wordList = fo.read().split('\n')
    fo.close()

    for word in wordList:
        # wordList内の各文字列のパターンを取得する.
        pattern = getWordPattern(word)

        if pattern not in allPatterns:
            allPatterns[pattern] = [word]
        else:
            allPatterns[pattern].append(word)

    # これはコードを作成するコードです.
    # wordPatterns.pyファイルには非常に大きな1つの代入文が含まれています.
    fo = open('wordPatterns.py', 'w')
    fo.write('allPatterns = ')
    fo.write(pprint.pformat(allPatterns))
    fo.close()


if __name__ == '__main__':
    main()