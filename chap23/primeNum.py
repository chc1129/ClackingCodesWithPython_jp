# 素数ふるい
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import math, random


def isPrimeTrialDiv(num):
    # 素数ならTrue、そうでなければFalseを返す.

    # 素数をテストするために試し割りアルゴリズムを使う.

    # 2より小さいすべての整数は素数ではない.
    if num < 2:
        return False

    # numが、numの平方根までの任意の数で割り切れるかどうかを調べる.
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def primeSieve(sieveSize):
    # エラトステネスのふるいのアルゴリズムを使って、
    # 素数のリストを返す.

    sieve = [True] * sieveSize
    sieve[0] = False # ゼロと1は素数ではない.
    sieve[1] = False

    # ふるいを作成する.
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i

    # 素数をまとめてリストにする.
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)

    return primes

def rabinMiller(num):
    # numが素数ならTrueを返す.
    if num % 2 == 0 or num < 2:
        return False # 偶数ではRabin-Millerが動作しない.
    if num == 3:
        return True
    s = num - 1
    t = 0
    while s % 2 == 0:
        # 奇数になるまで半分にする.
        # （sを半分にした回数を数えるためにtを使う）
        s = s // 2
        t += 1
    for trials in range(5): # numが素数でないことと疑い5回検算する.
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1: # vが1なら、このテストは適用されない.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

# ほとんどの場合、いくつかの数十の素数で割ることで、
# numが素数でないかどうかをすばやく判定できる.
# これは、すべての合成数を検知しないので、rabinMiller()より早く動作する.
LOW_PRIMES = primeSieve(100)


def isPrime(num):
    # numが素数ならTrueを返す.
    # rabinMiller()を呼ぶ前に、素数のチェックをする.
    if (num < 2):
        return False # 0、1、負の数は素数でない.
    # 小さい素数のいずれかがnumを分割できるかどうかを確認する.
    for prime in LOW_PRIMES:
        if (num == prime):
            return True
        if (num % prime == 0):
            return False
    # すべてが失敗したら、rabinMiller()を呼び素数かどうかを判定する.
    return rabinMiller(num)


def generateLargePrime(keysize=1024):
    # keysizeビットのランダムな素数を返す.
    while True:
        num = random.randrange(2**(keysize-1), 2**(keysize))
        if isPrime(num):
            return num
