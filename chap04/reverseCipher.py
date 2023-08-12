# 逆暗号
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

#message = 'Three can keep a secret, if two of them are dead.'
#message = '.daed era meht fo owt fi ,terces a peek nac eerhT'
message = input('Enter message: ')
#translated = ''


i = len(message) - 1
while i >= 0:
    translated = translated + message[i]
    print('i is ', i, ', message[i] is', message[i], ', translated is', translated)
    i = i - 1

print(translated)
