import random
from math import floor
from math import sqrt


# zjistime jestli je n prvocislo
def isPrime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, floor(sqrt(n))):
        if n % i == 0:
            return False
    return True


# najdeme nejvetsi spolecny delitel
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# rekurzivne najdeme inverzni modulo
def inverseModulus(a, b):
    if a == 0:
        return b, 0, 1

    g, x1, y1 = inverseModulus(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return g, x, y


minNumber = 1e3
maxNumber = 1e6


# vygenerujeme nahodne prvocislo z minNumber az maxNumber
def getPrime():
    num = 0
    while not isPrime(num):
        num = random.randint(minNumber, maxNumber)
    return num


# vygenerujeme par klicu -> privatni a verejny klic s pouzitim nahodnych prvocisel a inverzniho modula (vzorce z tabule)
def getKeys():
    p = getPrime()
    q = getPrime()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)

    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    d = inverseModulus(e, phi)[1]

    return (d, n), (e, n)


# funkce na sifrovani
def encrypt(key, text):
    e, n = key
    cipher = []
    for char in text:
        a = ord(char)
        cipher.append(pow(a, e, n))
    return cipher


# funkce na desifrovani
def decrypt(privateKey, cipher):
    text = ""
    d, n = privateKey
    for num in cipher:
        a = pow(num, d, n)
        text = text + str(chr(a))
    return text


if __name__ == "__main__":
    privateKey, publicKey = getKeys()

    print("Privatni klic:\n" + str(privateKey))
    print("Verejny klic:\n" + str(privateKey))

    text = "Kacka je fakt hodna holka!"
    print("Text: %s\n" % text)

    cipher = encrypt(publicKey, text)
    print("Sifrovany text: %s\n" % cipher)

    plain = decrypt(privateKey, cipher)
    print("Desifrovany text: %s\n" % plain)
