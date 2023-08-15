# 公開鍵暗号
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import sys, math

# makePublicPrivateKeys.pyによって、
# このプログラム用の公開鍵と秘密鍵が作成される.
# 鍵ファイルのある同じフォルダーで、このプログラムを実行する必要がある.

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def main():
    # メッセージをファイルに暗号化したり、
    # ファイルからメッセージを復号したりする.
    filename = 'encrypted_file.txt' # 読み書きするファイル.
    mode = 'encrypt' # 'encrypt'か'decrypt'のどちらかをセットする.

    if mode == 'encrypt':
        message = 'Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets. Gerald Priestland. The Founding Fathers gave the free press the protection it must have to bare the secrets of government and inform the people. Hugo Black.'
        pubKeyFilename = 'al_sweigart_pubkey.txt'
        print('Encrypting and writing to %s...' % (filename))
        encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)

        print('Encrypted text:')
        print(encryptedText)

    elif mode == 'decrypt':
        privKeyFilename = 'al_sweigart_privkey.txt'
        print('Reading from %s and decrypting...' % (filename))
        decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)

        print('Decrypted text:')
        print(decryptedText)


def getBlocksFromText(message, blockSize):
    # メッセージの文字列をブロック値のリストに変換する.
    for character in message:
        if character not in SYMBOLS:
            print('ERROR: The symbol set does not have the character %s' % (character))
            sys.exit()
    blockInts = []
    for blockStart in range(0, len(message), blockSize):
        # テキストのブロックからブロック値を計算する.
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(message))):
            blockInt += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize):
    # ブロック値のリストを元のメッセージ文字列に変換する.
    # 元のメッセージ長は、
    # 最後のブロック値を適切に変換するために必要である.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                # このブロック値から
                # 128文字（あるいはblockSizeに設定した値）のメッセージ文字列に戻す.
                charIndex = blockInt // (len(SYMBOLS) ** i)
                blockInt = blockInt % (len(SYMBOLS) ** i)
                blockMessage.insert(0, SYMBOLS[charIndex])
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize):
    # メッセージ文字列をブロック値のリストに変換し、各ブロック値を暗号化する.
    # 暗号化のために公開鍵を渡す.
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        # 暗号文 = 平文 ^ e mod n
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize):
    # 暗号化されたブロックのリストを元の文字列に復号する.
    # 元のメッセージ長は、最後のブロックを正しく復号するために必要である.
    # 復号するには秘密鍵を渡してください.
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        # 平文 = 暗号文 ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    # 公開鍵や秘密鍵を含むファイル名を与え、
    # 鍵をタプル(n,e)や(n,d)の形で返す.
    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=None):
    # 鍵ファイルの鍵を使って、メッセージを暗号化し、ファイルに保存する.
    # 暗号化されたメッセージを返す. 
    keySize, n, e = readKeyFile(keyFilename)
    if blockSize == None:
        # blockSizeが与えられていない場合、鍵長とシンボル集合のサイズによって最大値が設定される.
        blockSize = int(math.log(2 ** keySize, len(SYMBOLS)))
    # 鍵サイズがブロックサイズに対して十分大きいかどうかを確認する.
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?')
    # メッセージを暗号化する.
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)

    # 大きな整数値を1つの文字列に変換する.
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    # 暗号化された文字列を出力ファイルに書き込む.
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    fo = open(messageFilename, 'w')
    fo.write(encryptedContent)
    fo.close()
    # 暗号化された文字列を返す.
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    # 鍵ファイルの鍵を使って、ファイルから暗号化されたメッセージを読み込み、それを復号する.
    # 復号したメッセージを返す.
    keySize, n, d = readKeyFile(keyFilename)


    # メッセージ長と暗号化されたメッセージをファイルから読み込む.
    fo = open(messageFilename)
    content = fo.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    # 鍵サイズがブロックサイズに対して十分に大きいかを確認する.
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?')

    # 暗号化されたメッセージを大きな整数値に変換する.
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    # 大きな整数値を復号する.
    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)


# （モジュールとしてインポートする代わりに）publicKeyCipher.pyを実行すると、
# main()関数を呼び出す.
if __name__ == '__main__':
    main()
