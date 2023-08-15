# 公開鍵暗号の鍵生成
# https://www.nosharch.com/crackingcode/ (BSD Licensed)

import random, sys, os, primeNum, cryptomath


def main():
    # 1024ビットの公開鍵と秘密鍵を生成する.
    print('Making key files...')
    makeKeyFiles('al_sweigart', 1024)
    print('Key files made.')

def generateKey(keySize):
    # サイズがkeySizeビットである公開鍵・秘密鍵を生成する.
    p = 0
    q = 0
    # ステップ1:2つの素数pとqを生成する.n = p * qを計算する.
    print('Generating p & q primes...')
    while p == q:
        p = primeNum.generateLargePrime(keySize)
        q = primeNum.generateLargePrime(keySize)
    n = p * q

    # ステップ2:(p-1)*(q-1)と互いに素であるeを生成する.
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # 有効な値になるまで、乱数eを試し続ける.
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # ステップ3:eのモジュラー逆数を計算して、dとする.
    print('Calculating d that is mod inverse of e...')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    print('Public key:', publicKey)
    print('Private key:', privateKey)

    return (publicKey, privateKey)


def makeKeyFiles(name, keySize):
    # 2つのファイル'x_pubkey.txt'と'x_privkey.txt'(xはフィル名)を作成する.
    # それぞれのファイルには, nとeの組とnとdの組が記述されており,
    # この2つの数はカンマで区切られている.

    # 古い鍵が上書きされてしまうことを防ぐために、安全性チェックを設ける.
    if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name)):
        sys.exit('WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name or delete these files and re-run this program.' % (name, name))

    publicKey, privateKey = generateKey(keySize)

    print()
    print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing public key to file %s_pubkey.txt...' % (name))
    fo = open('%s_pubke.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()

    print()
    print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing private key to file %s_privkey.txt...' % (name))
    fo = open('%s_privkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    fo.close()


# （モジュールとしてインポートする代わりに）makePublicPrivateKeys.pyを実行すると、
# main()関数を呼び出す.
if __name__ == '__main__':
    main()
