# 転置式暗号の暗号化
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import pyperclip

def main():
    message = 'Common sense is not so comon.'
    key = 8

    ciphertext = encryptMessage(key, message)

    # 画面に暗号文を表示する
    # ただし、暗号化されたメッセージの終端には
    # パイプ文字を配置する.
    print(ciphertext + '|')

    # 暗号化された文字列をクリップボードにコピーする.
    pyperclip.copy(ciphertext)


def encryptMessage(key, message):
    # 暗号分の各文字列は格子の列を表す.
    ciphertext = [''] * key

    # ciphertextの各列でループする.
    for column in range(key):
        currentIndex = column

        # currentIndexがメッセージ長を超えるまでループを続ける.
        while currentIndex < len(message):
            # リストciphertextの現在の位置に、
            # messageにおけるcurrentIndexの位置にある文字を置く.
            ciphertext[column] += message[currentIndex]

            # currentIndexを次に移動する.
            currentIndex += key

    # 暗号文のリストを単一の文字列に変換して直す
    return ''.join(ciphertext)

# (モジュールとしてインポートする代わりに)transpositionEncrpyt.pyを実行すると、
# main()関数を呼び出す.
if __name__ == '__main__':
    main()
