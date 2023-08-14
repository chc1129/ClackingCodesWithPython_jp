# 単一換字式暗号の解読
# https://www.nostarch.com/crackingcodes (BSD Licensed)

import os, re, copy, pyperclip, simpleSubCipher, wordPatterns, makeWordPatterns





LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')

def main():
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'

    # 妥当な暗号文の変換の候補を決定する.
    print('Hacking...')
    letterMapping = hackSimpleSub(message)

    # ユーザーに結果を表示する
    print('Mapping:')
    print(letterMapping)
    print()
    print('Original ciphertext:')
    print(message)
    print()
    print('Copying hacked message to clipboard:')
    hackedMessage = decryptWithCipherletterMapping(message, letterMapping)
    pyperclip.copy(hackedMessage)
    print(hackedMessage)


def getBlankCipherletterMapping():
    # 暗号文字マッピングに用いる空の辞書を返す
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}


def addLettersToMapping(letterMapping, cipherword, candidate):
    # パラメーターletterMappingには暗号文字マッピングを保存した辞書を指定する.
    # マッピングは関数によってコピーされる.
    # パラメーターcipherwordには暗号単語を指定する.
    # パラメーターcandidateには,
    # 暗号単語であるcihperwordを復号したときの英単語の候補を指定する.

    # この関数は, candidate内の文字を
    # 暗号文字に対する復号文字の候補として,
    # 暗号文字マッピングに追加する.


    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:
            letterMapping[cipherword[i]].append(candidate[i])



def intersectMappings(mapA, mapB):
    # 2つのマップを交差させるために空のマップを作る.
    # 両方のマップに復号文字の候補が存在すれば,交差されたマップにはその重複した文字の候補だけを追加する.
    intersectedMapping = getBlankCipherletterMapping()
    for letter in LETTERS:

        # 空のリストは任意の文字が候補であることを意味する.
        # この場合, 他のマップを完全にコピーする.
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            # mapA[letter]内の文字がmapB[lette]内に存在すれば、
            # intersectedMapping[letter]にその文字を追加する.
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping


def removeSolvedLettersFromMapping(letterMapping):
    # 1文字にしかマッピングされていないとき、
    # その暗号文字は解決済みであり、他の文字から削除できる.
    # 例えば、'A'が候補['M', 'N']に、'B'が['N']にマッピングされていれば、
    # 'B'は'N'に常にマッピングすることがわかる.
    # そのため、'A'がマッピングしているリストから'N'を削除できる. よって、'A'は['M']にマッピングする.
    # 'A'は1つの文字にしかにマッピングしていないので、
    # 他の文字がマップしているリストに'M'が含まれていれば、それを削除できる.
    # このようにしてマッピングを縮小し続けるためにループする.

    loopAgain = True
    while loopAgain:
        # 最初はループしないと仮定する.
        loopAgain = False

        # solvedLettersはマッピングの候補が
        # 1つだけになった大文字のリストである.
        solvedLetters = []
        for cipherletter in LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])

        # もし文字が解読されれば
        # その文字は別の暗号文字に対する復号文字の候補にならない.
        # よって、他のリストから削除する必要がある
        for cipherletter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        # 新しい文字が解読されれば、再びループする.
                        loppAgain = True
    return letterMapping


def hackSimpleSub(message):
    intersectedMap = getBlankCipherletterMapping()
    cipherwordList = nonLettersOrSpacePattern.sub('', message.upper()).split()
    for cipherword in cipherwordList:
        # 暗号単語に対して、新しい暗号文字のマッピングを取得する.
        candidateMap = getBlankCipherletterMapping()

        wordPattern = makeWordPatterns.getWordPattern(cipherword)
        if wordPattern not in wordPatterns.allPatterns:
            continue # この単語は辞書になかったので、続行する.

        # 文字の候補をマッピングに追加する.
        for candidate in wordPatterns.allPatterns[wordPattern]:
            addLettersToMapping(candidateMap, cipherword, candidate)

        # 新しいマッピングと既存の交差マッピングを交差させる.
        intersectedMap = intersectMappings(intersectedMap, candidateMap)

    # 他のリストから解読済みの文字を削除する.
    return removeSolvedLettersFromMapping(intersectedMap)


def decryptWithCipherletterMapping(ciphertext, letterMapping):
    # 文字のマッピングを用いて、暗号文を復号した結果の文字列を返す.
    # ただし、完全に解読できない文字はアンダースコアで置き換える.

    # 最初にletterMappingから簡単なサブ鍵を作成する.
    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letterMapping[cipherletter]) == 1:
            # 1文字だけの場合は、それを鍵に追加する
            keyIndex = LETTERS.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    # 作成した鍵で暗号文を復号する.
    return simpleSubCipher.decryptMessage(key, ciphertext)


if __name__ == '__main__':
    main()
