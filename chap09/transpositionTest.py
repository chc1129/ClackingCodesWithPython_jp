# 転置式暗号のテスト
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import random, sys, transpositionEncrypt, transpositionDecrypt

def main():
    random.seed(42) # 固定のランダムシード値をセットする.

    for i in range(20): # 20回テストする.
        # テストするためにランダムなメッセージを生成する.

        # メッセージはランダムな長さを持つ.
        message = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' * random.randint(4, 40)

        # メッセージを攪拌するためにリストに変換する.
        message = list(message)
        random.shuffle(message)
        message = ''.join(message) # リストを文字列に戻す.

        print('Test #%s: "%s..."' % (i + 1, message[:50]))

        # 各メッセージに対する鍵の全候補を検証する.
        for key in range(1, int(len(message) / 2)):
            encrypted = transpositionEncrypt.encryptMessage(key, message)
            decrypted = transpositionDecrypt.decryptMessage(key, encrypted)

            # もし復号して元のメッセージと一致しなければ,
            # エラーを表示して終了する.
            if message != decrypted:
                print('Mismatch with key %s and message %s.' % (key, message))
                print('Decrypted as: ' + decrypted)
                sys.exit()

    print('Transposition cipher test passed.')


# (モジュールとしてインポートする代わりに) transpositionTest.pyを実行すると.
# main()関数を呼び出す.
if __name__ == '__main__':
    main()
