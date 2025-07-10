import des_utility
import des

# This is the Triple DES (DES3) implementation with CTR.
# This class can be instantiated with 3 keys and uses 3 simple DES instances internally.
# Each simple DES internal instance uses one key out of the 3 provided. 
class DES3CipherCTR:
    def __init__(self, key1, key2, key3):
        # Because this is Triple DES, we use internally 3 simple DES instances
        self.des1 = des.DESCipher(key1)
        self.des2 = des.DESCipher(key2)
        self.des3 = des.DESCipher(key3)

    # This method applies triple DES encryption.
    def encryptBlock(self, bits):
        # Encrypt with 'key1' (because 'des1' uses 'key1')
        step1Block = self.des1.encript(bits)

        # Decrypt the result of the previous encription with 'key2' (because 'des2' uses 'key2')
        step2Block = self.des2.decript(step1Block)

        # Encrypt the result of the previous decription with 'key3' (because 'des3' uses 'key3')
        step3Block = self.des3.encript(step2Block)

        # The final result is the block obtained after the 3rd step
        return step3Block

    # This method basically applies the opposite operations of the encryptBlock() method and in reverse order.
    def decryptBlock(self, bits):
        # Decrypt with 'key3' (because 'des3' internally uses 'key3')
        step1Block = self.des3.decript(bits)

        # Encrypt the result of the previous decription with 'key2' (because 'des2' internally uses 'key2')
        step2Block = self.des2.encript(step1Block)

        # Decrypt the result of the previous encription with 'key1' (because 'des1' internally uses 'key1')
        step3Block = self.des1.decript(step2Block)

        return step3Block

    # Counter mode encryption for Triple DES (CTR) implementation.
    # CTR turns a block cipher into a stream cipher, which allows to encrypt plaintexts of any length.
    # This method uses a 'nonce', which is fixed binary number in string format.
    # The counter value for each input block is generated from the 'nonce' and a number represented as
    # a string, which ensures every input block is unique.
    def encryptCTR(self, plaintext, nonce):
        # Convert plaintext to bitstring
        plaintextBits = des_utility.string2Bits(plaintext)

        blocks = []
        # Iterate between 0 and len(plaintextBits), with a step of 64
        for i in range(0, len(plaintextBits), 64):
            block = plaintextBits[i:i+64]
            blocks.append(block)
        
        ciphertextBits = ""
        for i, block in enumerate(blocks):
            # Construct counter block: nonce (32 bits) + counter (32 bits)
            counter = format(i, '032b')

            inputBlock = nonce + counter
            keystream = self.encryptBlock(inputBlock)
            xorResult = self.xor(block.ljust(64, '0'), keystream)[:len(block)]
            ciphertextBits += xorResult

        return ciphertextBits
    
    # Counter mode decryption for Triple DES (CTR) implementation.
    # This method also uses a 'nonce' bynary string, just like the encryptCTR() method.
    def decryptCTR(self, ciphertextBits, nonce):
        blocks = []
        # Iterate between 0 and len(ciphertextBits), with a step of 64
        for i in range(0, len(ciphertextBits), 64):
            block = ciphertextBits[i:i+64]
            blocks.append(block)
        
        plaintextBits = ""
        for i, block in enumerate(blocks):
            # Construct counter block: nonce (32 bits) + counter (32 bits) (Same as in encryption)
            counter = format(i, '032b')

            inputBlock = nonce + counter
            keystream = self.encryptBlock(inputBlock)
            xorResult = self.xor(block.ljust(64, '0'), keystream)[:len(block)]
            plaintextBits += xorResult

        return des_utility.bits2String(plaintextBits)
    
        
    # Method which applies XOR to 2 binary numbers represented as strings.
    def xor(self, bits1, bits2):
        result = ''

        # Generate an array of pairs (tuples) from the 2 strings by using the zip() function.
        # The zip() function creates pairs from 2 
        # For example, if a = '1234' and b = 'abcd', then zip(a, b) will return:
        # {'1a', '2b', '3c', '4d'}
        bitsPairs = zip(bits1, bits2)
        for b1, b2 in bitsPairs:
            if b1 == b2:
                result += '0'
            else:
                result += '1'

        return result
    

def main():
    # Text to be encrypted
    plaintext = "DES3 Algorithm test with text of arbitrary length"

    # Create a 32 bits 'nonce' (number used once). We use the same 'nonce' for both encryption and decryption.
    # The 'nonce' should be used only once for a specific plainttext/ciphertext.
    nonce = "10101010101010101010101010101010"
    # Then pad the 'nonce' to 64 bits
    nonce = nonce.zfill(64)

    # The 3 keys used in the DES3 algorithm.
    # These keys are 64 bit and have to string made of 16 hexadecimals characters
    # (characters between 0-9 and A-F) and are concatenated from two 8-character strings
    # just for ease of reading.
    key1 = "12305709" + "9BACD2F1"
    key2 = "21D0E319" + "BA56E604"
    key3 = "D1A253FF" + "ABC00213"

    # Create a DES3 instance which uses the 3 keys
    des3CTR = DES3CipherCTR(key1, key2, key3)

    # Encrypt
    cipherBits = des3CTR.encryptCTR(plaintext, nonce)

    # Decrypt
    decryptedText = des3CTR.decryptCTR(cipherBits, nonce)

    print("Original text:", plaintext)
    print("Decrypted text:", decryptedText)

    # Verify if decrypted text matches the original plaintext
    if decryptedText == plaintext:
        print("Decryption successful!")
    else:
        print("Decryption failed")

if __name__ == "__main__":
    main()