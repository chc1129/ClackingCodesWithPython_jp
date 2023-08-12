# シーザー暗号の解読
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

message = 'guv6Jv6Jz!J6rp5r7Jzr66ntrM'
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

# 候補となるすべての鍵でループする.
for key in range(len(SYMBOLS)):
    # 先の反復のtranslatedの値をクリアするために,
    # translatedに空文字列をセットするのは重要である.
    translated = ''

    # 残りのプログラムはシーザー暗号のプログラムとほぼ同様である.

    # message内の各シンボルでループする.
    for symbol in message:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)
            translatedIndex = symbolIndex - key

            # ラップアラウンドを処理する.
            if translatedIndex < 0:
                translatedIndex = translatedIndex + len(SYMBOLS)

            # 解読したシンボルを追加する.
            translated = translated + SYMBOLS[translatedIndex]

        else:
            # 暗号化・復号せずにシンボルを追加する.
            translated = translated + symbol

    # 全ての復号結果の候補を表示する.
    print('key #%s: %s' % (key, translated))
