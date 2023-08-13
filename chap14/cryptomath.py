# Cryptomathモジュール
# https://www.nostarch.com/crackingcodes (BSD Licensed)

def gcd(a, b):
    # ユークリッドのアルゴリズムを用いてaとbのGCDを返す.
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    # a*x % m = 1を満たすxである、
    # モジュラーmにおけるaのモジュラー逆元を返す.

    if gcd(a, m) != 1:
        return None #　aとmが互いに素でないなら、モジュラー逆数は存在しない.

    # ユークリッドの拡張アルゴリズムを使って計算する.
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # //は整数除算演算子であることに注意する.
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m