# Utility functions that convert from string to bits and viceversa.
# These functions were provided by the professor at the lab, they're not personal work.

def string2Bits(text):
     bits = ""
     for letter in text:
          tmpBits = bin(ord(letter))[2:]
          # fill tmpBits to 0 to left side to make len = 8
          if len(tmpBits) != 8:
               tmpBits = "0"*(8-len(tmpBits)) + tmpBits
          bits = bits+tmpBits
     return bits
 
def bits2String(bits):
     text = ""
     for i in range(0, len(bits), 8):
          tmpBits = bits[i:i+8]
          order   = int(tmpBits, 2)
          text = text + chr(order)
     return text