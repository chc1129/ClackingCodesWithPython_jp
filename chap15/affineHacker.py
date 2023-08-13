# アフィン暗号の解読
# https://www.nostarch.com/crackingcodes (BSD Licensed)

import pyperclip, affineCipher, detectEnglish, cryptomath

SILENT_MODE = False

def main():
    # https://www.nostarch.com/crackingcodes/にあるソースコードから
    # このテキストをコピー＆ペーストしてください.
    myMessage = """"5QG9ol3La6QI93!xQxaia6faQL9QdaQG1!!axQARLa!!AuaRLQADQALQG93!xQxaGaAfaQ1QX3o1RQARL9Qda!AafARuQLX1LQALQI1iQX3o1RN"Q-5!1RQP36ARu"""

    hackedMessage = hackAffine(myMessage)

    if hackedMessage != None:
        # 便宜のために平文を画面に表示する.
        # 解読したメッセージをクリップボードにコピーする.
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption.')


def hackAffine(message):
    print('Hacking...')

    # Pythonプログラムはいつでも
    # Ctrl-C(Windowsの場合)あるいはCtrl-D(macOSやLinuxの場合)で終了できる.
    print('Press Ctrl-C or Ctrl-D to quit at any time.)')

    # 鍵の全候補でループして総当たりする.
    for key in range(len(affineCipher.SYMBOLS) ** 2):
        keyA = affineCipher.getKeyParts(key)[0]
        if cryptomath.gcd(keyA, len(affineCipher.SYMBOLS)) != 1:
            continue

        decryptedText = affineCipher.decryptMessage(key, message)
        if not SILENT_MODE:
            print('Tried Key %s... (%s)' % (key, decryptedText[:40]))

        if detectEnglish.isEnglish(decryptedText):
            # これが正しい復号であるかをユーザーに尋ねる.
            print()
            print('Possible encryption hack:')
            print('Key: %s' % (key))
            print('Decrypted message: ' + decryptedText[:200])
            print()
            print('Enter D if done, anything else to continume hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText
    return None


# (モジュールとしてインポートする代わりに)affineHacker.pyを実行すると,
# main()関数を呼び出す.
if __name__ == '__main__':
    main()
