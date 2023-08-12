# 転置式ファイル暗号
# https://www.nostarch.com/crackingcodes/ (BSD License)

import time, os, sys, transpositionEncrypt, transpositionDecrypt

def main():
    inputFilename = 'frankenstein.txt'
    # 注意!outputFilenameというファイルがすでに存在する場合.
    # そのファイルは上書きされる.
    outputFilename = 'frankenstein.encrypted.txt'
    myKey = 10
    myMode = 'encrypt' # 'encrypt'または'decrypt'をセットする.

    # 入力ファイルが存在しない場合, プログラムはすぐに終了する.
    if not os.path.exists(inputFilename):
        print('The file %s does not exist. Quitting...' % (inputFilename))
        sys.exit()

    # 出力ファイルがすでに存在する場合, ユーザーに終了する機会を与える.
    if os.path.exists(outputFilename):
        print('This will overwrite the file %s. (C)ontinue or (Q)uit?' % (outputFilename))
        response = input('> ')
        if not response.lower().startswith('c'):
            sys.exit()

    # 入力ファイルからメッセージを読み込む.
    fileObj = open(inputFilename)
    content = fileObj.read()
    fileObj.close()

    print('%sing...' % (myMode.title()))

    # 暗号化・復号に要する時間を測定する
    startTime = time.time()
    if myMode == 'encrypt':
        translated = transpositionEncrypt.encryptMessage(myKey, content)
    elif myMode == 'decrypt':
        translated = transpositionDecrypt.decryptMessage(myKey, content)
    totalTime = round(time.time() - startTime, 2)
    print('%sion time: %s seconds' % (myMode.title(), totalTime))

    # 変換したメッセージをファイルに出力する
    outputFileObj = open(outputFilename, 'w')
    outputFileObj.write(translated)
    outputFileObj.close()

    print('Done %sing %s (%s characters).' % (myMode, inputFilename, len(content)))
    print('%sed file is %s.' % (myMode.title(), outputFilename))


# (モジュールとしてインポートする代わりに) transpositionCipherFile.pyを実行すると,
# main()関数を呼び出す.
if __name__ == '__main__':
    main()
