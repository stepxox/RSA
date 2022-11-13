import random
from math import floor
from math import sqrt
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic
 
qtCreatorFile = "rsa_kantor.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow, Ui_MainWindow):
                              
   # zjistime jestli je n prvocislo
   def isPrime(self, n):
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


   minNumber = 1e3
   maxNumber = 1e6


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
       self.labelN.setText(n)
       phi = (p - 1) * (q - 1)

       e = random.randrange(1, phi)

       while self.gcd(e, phi) != 1:
           e = random.randrange(1, phi)

       self.labelE.setText(e)
       d = self.inverseModulus(e, phi)[1]
       self.labelN.setText(d)

       return (d, n), (e, n)


   # funkce na sifrovani
   def encrypt(self, key, text):
       text = self.inputText.text()
       e, n = key
       cipher = []
       for char in text:
           a = ord(char)
           cipher.append(pow(a, e, n))
       self.finalText.setText(text)


   # funkce na desifrovani
   def decrypt(self, privateKey, cipher):
       text = self.inputText.text()
       d, n = privateKey
       for num in cipher:
           a = pow(num, d, n)
           text = text + str(chr(a))
       self.finalText.setText(text)


   #if __name__ == "__main__":
       #privateKey, publicKey = getKeys()
       #
      # print("Privatni klic:\n" + str(privateKey))
      # print("Verejny klic:\n" + str(privateKey))
      #
       #text = "cigan cerny"
       #print("Text: %s\n" % text)
       #
       #cipher = encrypt(publicKey, text)
       #print("Sifrovany text: %s\n" % cipher)
       #
       #plain = decrypt(privateKey, cipher)
       #print("Desifrovany text: %s\n" % plain)
    
   def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.encrypt.clicked.connect(self.encrypt)
        self.decrypt.clicked.connect(self.decrypt)
        
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
