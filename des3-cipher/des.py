import des_constants

# The implementation of the single DES algorithm.
# This implementation was provided by the professor at the lab, it's not personal work.
class DESCipher:

    def __init__(self,key):
        self._key = key
        # transform 16 hexadigits key in 64 bits
        self._key = bin(int(self._key, 16))[2:]
        self._key = "0"*(64-len(self._key)) + self._key
 
    # generate an array of keys
    def generateKeys(self):
        # generate key56 from self._key
        key56 = ""
        for i in range(len(des_constants.pc1)):
            key56 += self._key[des_constants.pc1[i]-1]
 
        # divide key56 in left and right
        left, right = key56[:28], key56[28:]
 
        keys = []
 
        # 16 rounds of repetition
        for i in range(16):
            if i in [0, 1, 8, 15]:
                left = left[1:]+left[:1]
                right = right[1:]+right[:1]
            else:
                left = left[2:]+left[:2]
                right = right[2:]+right[:2]
 
            tmpKey56 = left+right
 
            # generate key48 from tmpKey56
            key48 =  ""
            for j in range(len(des_constants.pc2)):
                key48 += tmpKey56[des_constants.pc2[j]-1]
 
            keys.append(key48)
        return keys
 
    # function f for the feistel network
    def f(self, step, right32, key48):
        # expand right32 to 48 bits
        right48 = ""
        for i in range(len(des_constants.exp)):
            right48 += right32[des_constants.exp[i]-1]
 
        # make xor between right48 and key48
        tmp48 = ""
        for i in range(48):
            tmp48 += str(int(right48[i]) ^ int(key48[i]))
 
        bits32 = ""
 
        for i in range(0, 48, 6):
            # get the 6 bits
            bit6 = tmp48[i:i+6]
            row = int(bit6[0]+bit6[5],2)
            col = int(bit6[1:5],2)
 
 
 
            # use lookup table S to generate bit4
            bit4 = bin(des_constants.sbox[i//6][row][col])[2:]
 
            bit4 = "0"*(4-len(bit4)) + bit4
 
            bits32 += bit4
 
        result32 = ""
 
        for i in range(len(des_constants.per)):
            result32 += bits32[des_constants.per[i]-1]
 
        return result32
 
    # encript des using 16 round of encription
    def encript(self, plaintext):
        # apply IP
        text64 = ""
        for i in range(len(des_constants.initial_perm)):
            text64 += plaintext[des_constants.initial_perm[i]-1]
 
        # generate the keys
        keys = self.generateKeys()
 
        # split text64 into left and right
        left32, right32 = text64[:32], text64[32:]
 
        # repeat 16 times
        for i in range(16):
            newL32 = right32
 
            tmp32 = self.f(i, right32, keys[i])
            newR32 = ""
            for i in range(32):
                newR32 += str(int(tmp32[i]) ^ int(left32[i]))
            left32, right32 = newL32, newR32
 
        text64 = left32+right32
 
        # apply the last permutation
        ciphertext = ""
        for i in range(len(des_constants.final_perm)):
            ciphertext += text64[des_constants.final_perm[i]-1]
 
        return ciphertext
 
    def decript(self, ciphertext):
          # apply inverse_per to ciphertext
          text64 = ""
          for i in range(64):
               text64 += ciphertext[des_constants.initial_perm[i]-1]
 
          # generate keys
          keys = self.generateKeys()
 
          # 16 round of decript
          left32, right32 = text64[:32], text64[32:]
 
          for i in range(15, -1, -1):
               newR32 = left32
 
               temp32 = self.f(i, left32, keys[i])
 
               newL32 = ""
               for i in range(32):
                    newL32 += str(int(temp32[i]) ^ int(right32[i]))
 
               left32, right32 = newL32, newR32
 
          text64 = left32+right32
          plaintext = ""
          for i in range(64):
               plaintext += text64[des_constants.final_perm[i]-1]
 
          return plaintext