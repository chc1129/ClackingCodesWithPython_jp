# 転置式暗号の復号
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import math, pyperclip

def main():
    myMessage = 'Cenoonommstmme oo snnio. s s c'
    myKey = 8

    plaintext = decryptMessage(myKey, myMessage)

    # 復号するメッセージの末尾に空白があることを想定して,
    # パイプ文字を表示する
    print(plaintext + '|')

    pyperclip.copy(plaintext)


def decryptMessage(key, message):
    # 転置式暗号の復号関数は,
    # 文字列のリストにより格子をシミュレートしてヘイブンを取得する.
    # まずはいくつかの値を計算する必要がある.

    # 格子の列数.
    numOfColumns = int(math.ceil(len(message) / float(key)))
    # 格子の行数
    numOfRows = key
    # 格子の最後の列にある影付きの箱の数.
    numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)

    # plaintextの各文字列あ格子の列を表す.
    plaintext = [''] * numOfColumns

    # 変数columnとrowは
    # 暗号文の文字を格子のどこにいれるかを示す.
    column = 0
    row = 0

    for symbol in message:
        plaintext[column] += symbol
        column += 1 # 次の列を指す.

        # 列がなくなった場合や,影付きの箱にいる場合は
        # 次の行の1列目に移動する
        if (column == numOfColumns) or (column == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            column = 0
            row += 1

    return ''.join(plaintext)

# (モジュールとしてインポートする代わりに) transpositionDecrypt.pyを実行すると,
# main()関数を呼び出す
if __name__ == '__main__':
    main()
