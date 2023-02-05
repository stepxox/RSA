import random
from math import floor
from math import sqrt
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic
 
qtCreatorFile = "rsa_kantor.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow, Ui_MainWindow):
    _known_primes = [2, 3]
                              
    def _try_composite(self, a, d, n, s):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i *d, n) == n-1:
                return False
        return True
    
    def isPrime(self, n, _precision_for_huge_n=16):
        if n in self._known_primes:
            return True
        if any((n % p) == 0 for p in self._known_primes) or n in (0, 1):
            return False
        d, s = n - 1, 0
        while not d % 2:
            d, s = d >> 1, s + 1
        if n < 1373653: 
            return not any(self._try_composite(a, d, n, s) for a in (2, 3))
        if n < 25326001: 
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5))
        if n < 118670087467: 
            if n == 3215031751: 
                return False
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7))
        if n < 2152302898747: 
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
        if n < 3474749660383: 
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
        if n < 341550071728321: 
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
        return not any(self._try_composite(a, d, n, s) 
                       for a in self._known_primes[:_precision_for_huge_n])
    
   # zjistime jestli je n prvocislo
   #def isPrime(self, n):
   #    if n < 2:
   #        return False
   #    if n == 2:
   #       return True
   #    if n % 2 == 0:
   #        return False
   #    for i in range(3, floor(sqrt(n))):
   #        if n % i == 0:
   #            return False
   #    return True


    # najdeme nejvetsi spolecny delitel
    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a


    # rekurzivne najdeme inverzni modulo
    def inverseModulus(self, a, b):
        if a == 0:
            return b, 0, 1
 
        g, x1, y1 = self.inverseModulus(b % a, a)
 
        x = y1 - (b // a) * x1
        y = x1
 
        return g, x, y


    minNumber = 1*10**18
    maxNumber = 1*10**19-1


    # vygenerujeme nahodne prvocislo z minNumber az maxNumber
    def getPrime(self):
        num = 0
        while not self.isPrime(num):
            num = random.randint(self.minNumber, self.maxNumber)
        return num


    # vygenerujeme par klicu -> privatni a verejny klic s pouzitim nahodnych prvocisel a inverzniho modula (vzorce z tabule)
    def getKeys(self):
        p = self.getPrime()
        q = self.getPrime()
 
        n = p * q
        self.lineEdit_n.setText(str (n))
        phi = (p - 1) * (q - 1)
 
        e = random.randrange(1, phi)
 
        while self.gcd(e, phi) != 1:
            e = random.randrange(1, phi)
 
        self.lineEdit_e.setText(str (e))
        d = self.inverseModulus(e, phi)[1]
        self.lineEdit_d.setText(str (d))
    
    def encrypt(self):
        text = self.inputText.text()
        X = 12
        Z = 10
        blocks = Z * X
        n = int(self.lineEdit_n.text())
        e = int(self.lineEdit_e.text())
        textblocks = [ord(char) for char in text]
        BINblocks = [bin(ch)[2:].zfill(X) for ch in textblocks]
        BIN = "".join(BINblocks)
        BINs = [BIN[i:i + blocks] for i in range(0, len(BIN), blocks)]
        INTblocks = [int(ch, 2) for ch in BINs]
        c = [pow(ch, e, n) for ch in INTblocks]
        c = " ".join([str(ch) for ch in c])
        self.finalText.setText(c)
    
    
    def decrypt(self):
        cipher = self.inputText.text()
        X = 12
        Z = 10
        blocks = Z * X
        d = int(self.lineEdit_d.text())
        n = int(self.lineEdit_n.text())
        textblocks = [int(ch) for ch in cipher.split(" ")]
        m = [pow(c, d, n) for c in textblocks]
        BINblocks = [bin(ch)[2:].zfill(blocks) for ch in m]
        BIN = "".join(BINblocks)
        BINs = [BIN[i:i + X] for i in range(0, len(BIN), X)]
        INTs = [int(ch, 2) for ch in BINs]
        output = [chr(ch) for ch in INTs]
        output = "".join(output)
        self.finalText.setText(output)

    
    def __init__(self):
         QMainWindow.__init__(self)
         Ui_MainWindow.__init__(self)
         self.setupUi(self)
         self.encrypt_button.clicked.connect(self.encrypt)
         self.decrypt_button.clicked.connect(self.decrypt)
         self.random.clicked.connect(self.getKeys)
        
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
