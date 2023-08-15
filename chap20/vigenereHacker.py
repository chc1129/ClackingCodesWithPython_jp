# ヴィジュネル暗号の解読
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import itertools, re
import vigenereCipher, pyperclip, freqAnalysis, detectEnglish

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_KEY_LENGTH = 16 # これより長い鍵は試行しない.
NUM_MOST_FREQ_LETTERS = 4 # 試行する各サブ鍵の候補の数.
SILENT_MODE = False # Trueにセットするとプログラムは何も表示しない.
NONLETTERS_PATTERN = re.compile('[^A-Z]')


def main():
    # この暗号文を入力するのではなく、
    # https://www.nostarch.com/crackingcodes/からコピー＆ペーストする.
    ciphertext = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""
    hackedMessage = hackVigenere(ciphertext)

    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption.')


def findRepeatSequencesSpacings(message):
    # メッセージをたどり、3文字から5文字の反復を探す.
    # キーに反復、値にスペーシング（反復間の文字数）のリスト
    # を持つ辞書を返す.

    # 正規表現を使って、messageから非アルファベット文字を取り除く.
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # message内で見つかった文字列であるseqLenのリストをまとめる.
    seqSpacings = {} # キーは文字列、値はスペーシングの値のリスト.
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # 反復を決定し、それをseqに格納する.
            seq = message[seqStart:seqStart + seqLen]

            # messageの残りの部分で、この反復を探す.
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # 反復が見つかった.
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] # 空のリストで初期化する.

                    # 反復の間隔であるスペーシングを
                    # 追加する.
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getUsefulFactors(num):
    # 有効な因数のリストを返す.
    # ここでいう「有用」とは、MAX_KEY_LENGTH + 1未満であり、1ではないことを意味する.
    # 例えば、getUsefulFactors(144)は[2, 3, 4, 6, 8, 9, 12, 16]を返す.

    if num < 2:
        return [] # 2より小さい数は、有効な因数を持たない.

    factors = [] # 見つかった因数のリスト.

    # 因数が見つかったとき、
    # MAX_KEY_LENGTHまでの整数かを確認する.
    for i in range(2, MAX_KEY_LENGTH + 1): # 1は有用でないので、テストしない.
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)
            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors)) # 重複する因数を削除する.


def getItemAtIndexOne(items):
    return items[1]


def getMostCommonFactors(seqFactors):
    # まず、seqFactorsに含まれる各因数の数をカウントする.
    factorCounts = {} # キーは因数、値は因数の数.

    # seqFactorsのキーは反復する文字列であり、
    # 値はスペーシングの因数のリストである.
    # seqFactorsは{'GFD': [2, 3, 4, 6, 9, 12, 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}のような値を持つ.
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # 次に、因数とその因数の登場回数をタプルにセットし、それらのリストを作成する.
    # タプルなのでソート可能.
    factorsByCount = []
    for factor in factorCounts:
        # MAX_KEY_LENGTHより大きい因数を除外する.
        if factor <= MAX_KEY_LENGTH:
            # factorsByCountはタプル(factor, factorCount)のリストである.
            # factorsByCountは[(3, 497), (2, 487), ...]のような値を持つ.
            factorsByCount.append( (factor, factorCounts[factor]) )

    # 因数の数でリストをソートする.
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount


def kasiskiExamination(ciphertext):
    # 暗号文から
    # 複数回登場する3～5文字の反復を見つける.
    # repeatedSeqSpacingsは{'EXG': [192], 'NAF': [339, 972, 633], ... }のような値を持つ.
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)

    # (seqFactorsの説明については、getMostCommonFactors()を参照せよ)
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    # (factorsByCountの説明については、getMostCommonFactors()を参照せよ)
    factorsByCount = getMostCommonFactors(seqFactors)

    # factorsByCountから因数の数を得て、
    # それらをallLikelyKeyLengthsに入れる.
    # こうすることで、後で使用するときに便利になる.
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])

    return allLikelyKeyLengths


def getNthSubkeysLetters(nth, keyLength, message):
    # テキスト内にてn番目の文字から開始して、keyLengthごとの文字から構成される文字列を返す.
    # 例えば、getNthSubkeysLetters(1, 3, 'ABCABCABC')は、'AAA'を返す.
    #         getNthSubkeysLetters(2, 3, 'ABCABCABC')は、'BBB'を返す.
    #         getNthSubkeysLetters(3, 3, 'ABCABCABC')は、'CCC'を返す.
    #         getNthSubkeysLetters(1, 5, 'ABCDEFGHI')は、'AF'を返す.

    # 正規表現を使って、メッセージから非アルファベット文字を取り除く.
    message = NONLETTERS_PATTERN.sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    # 鍵の各文字に対して、もっとも可能性の高い文字を決定する.
    ciphertextUp = ciphertext.upper()
    # allFreqScoresはリストのリストであり、mostLikelyKeyLength個の要素を持つ.
    # これの内部のリストはリストfreqScoresである.
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)

        # freqScoresは次のようなタプルのリストである.
        # [(<サブ鍵の文字>, <頻度マッチスコア>), ... ]
        # リストは、頻度マッチスコアでソートされている.スコアが高いほど英語と一致することを意味する.
        # freqAnalysis.py内のenglishFreqMatchScore()のコメントを参照せよ.
        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = vigenereCipher.decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, freqAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        # 頻度マッチスコアでソートする.
        freqScores.sort(key=getItemAtIndexOne, reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            # 最初の文字を0番目の文字と表記するのはおかしいので、i + 1を使う.
            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print() # 改行を出力する.

    # 可能性の高いサブ鍵の
    # すべての組み合わせを試す.
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        # allFreqScores内の文字から鍵の候補を作成する.
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]

        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))

        decryptedText = vigenereCipher.decryptMessage(possibleKey, ciphertextUp)

        if detectEnglish.isEnglish(decryptedText):
            # 解読した暗号文を元の大文字・小文字に戻す.
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)

            # 鍵が見つからなかったかどうかを確認する.
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200]) # 最初の200文字だけを表示する.
            print()
            print('Enter D if done, anything else to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

    # 復号結果が英文のように見えなければ、Noneを返す.
    return None


def hackVigenere(ciphertext):
    # まず、カシスキー検査をして、
    # 暗号文の鍵長を調べる.
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Kasiski Examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            break

    # カシスキー検査で鍵長が見付からなかったら、
    # 鍵長を総当たり攻撃する.
    if hackedMessage == None:
        if not SILENT_MODE:
            print('Unable to hack message with likely key length(s). Brute forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # カシスキー検査ですでに試みた鍵長は再チェックしない.
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage != None:
                    break
    return hackedMessage


# (モジュールとしてインポートする代わりに)vigenereHacker.pyを実行すると
# main()関数を呼び出す.
if __name__ == '__main__':
    main()
