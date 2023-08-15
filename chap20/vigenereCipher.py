# ヴィジュネル暗号（多表式暗号）
# https://www.nostarch.com/crackingcodes (BSD Licensed)

import pyperclip

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    # このテキストはhttps://www.nostarch.com/crackingcode/からダウンロードできる.
    myMessage = """Alan Mathison Turing was a British mathematician, logician, cryptanalyst, and computer scientist."""
    myKey = 'ASIMOV'
    myMode = 'encrypt' # 'encrypt'か'decrypt'のどちらかをセットする.

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)

    print('%sed message:' % (myMode.title()))
    print(translated)
    pyperclip.copy(translated)
    print()
    print('The message has been copied to the clipboard.')


def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
    translated = [] # 暗号化・復号されたメッセージ文字列を格納する.

    keyIndex = 0
    key = key.upper()

    for symbol in message: # メッセージ内の各文字でループする.
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1はsymbol.upper()がLETTERS内に存在しないことを意味する.
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) # 暗号化なら追加する.
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) # 復号なら取り除く.

            num %= len(LETTERS) # ラップアラウンド処理する.

            # translatedの末尾に暗号化・復号した文字を追加する.
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1 # keyの次の文字に移動する.
            if keyIndex == len(key):
                keyIndex = 0

        else:
            # 暗号化・復号をせずに文字を追加する.
            translated.append(symbol)

    return ''.join(translated)

# (モジュールとしてインポートする代わりに)vigenereCipher.pyを実行すると,
# main()関数を呼び出す.
if __name__ == '__main__':
    main()
