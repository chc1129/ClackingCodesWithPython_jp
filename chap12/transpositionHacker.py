# 転置式暗号の解読
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import pyperclip, detectEnglish, transpositionDecrypt

def main():
    # https://www.nostach.com/crackingcodes/にあるソースコードから
    # このテキストをコピー&ペーストしてください.
    myMessage = """AaKoosoeDe5 b5sn ma reno ora'lhlrrceey e  enlh na  indeit n uhoretrm au ieu v er Ne2 gmanw,forwnlbsya apor tE.no euarisfatt  e mealefedhsppmgAnlnoe(c -or)alat r lw o eb  nglom,Ain one dtes ilhetcdba. t tg eturmudg,tfl1e1 v  nitiaicynhrCsaemie-sp ncgHt nie cetrgmnoa yc r,ieaa  toesa- e a0m82e1w shcnth  ekh gaecnpeutaaieetgn iodhso d ro hAe snrsfcegrt NCsLc b17m8aEheideikfr aBercaeu thllnrshicwsg etriebruaisss  d iorr."""

    hackedMessage = hackTransposition(myMessage)

    if hackedMessage == None:
        print('Failed to hack encryption.')
    else:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)

def hackTransposition(message):
    print('Hacking...')

    # PythonプログラムはCtrl-C(Windowsの場合)あるいは
    # Ctrl-D(macOSやLinuxの場合)を押していつでも停止できる.
    print('(Press Ctrl-C(on Windows) or Ctrl-D(on macOS and Linux) to quit at any time.)')

    # 鍵の全候補でループして総当たりする.
    for key in range(1, len(message)):
        print('Trying key #%s...' % (key))

        decryptedText = transpositionDecrypt.decryptMessage(key, message)

        if detectEnglish.isEnglish(decryptedText):
            # これが正しい復号であるかをユーザに尋ねる.
            print()
            print('Possible encryption hack:')
            print('Key %s: %s' % (key, decryptedText[:100]))
            print()
            print('Enter D if done, anything else to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

    return None

if __name__ == '__main__':
    main()
