import des_utility
import des

# This is the Triple DES (DES3) implementation withouth CTR or CBC.
# This class can be instantiated with 3 keys and uses 3 simple DES instances internally.
# Each simple DES internal instance uses one key out of the 3 provided. 
class DES3CipherSimple:
    def __init__(self, key1, key2, key3):
        # Create 3 DES instances, each with it's own key
        self.des1 = des.DESCipher(key1)
        self.des2 = des.DESCipher(key2)
        self.des3 = des.DESCipher(key3)

    def encrypt(self, plaintextBits):
        # Encrypt with 'key1' (because 'des1' uses 'key1')
        step1Block = self.des1.encript(plaintextBits)

        # Decrypt the result of the previous encription with 'key2' (because 'des2' uses 'key2')
        step2Block = self.des2.decript(step1Block)

        # Encrypt the result of the previous decription with 'key3' (because 'des3' uses 'key3')
        step3Block = self.des3.encript(step2Block)

        return step3Block

    def decrypt(self, ciphertextBits):
        # Decrypt with 'key3' (because 'des3' internally uses 'key3')
        step1Block = self.des3.decript(ciphertextBits)

        # Encrypt the result of the previous decription with 'key2' (because 'des2' internally uses 'key2')
        step2Block = self.des2.encript(step1Block)

        # Decrypt the result of the previous encription with 'key1' (because 'des1' internally uses 'key1')
        step3Block = self.des1.decript(step2Block)

        return step3Block
    

def main():
    # Text to be encrypted
    plaintext = "01234567"  # 8 ASCII characters = 64 bits
    print(f"Original text: {plaintext}")

    # Convert plaintext to bitstring
    plaintextBits = des_utility.string2Bits(plaintext)
    print(f"Plaintext bits: {plaintextBits}")

    # The 3 keys used in the DES3 algorithm.
    # These keys are 64 bit and have to string made of 16 hexadecimals characters
    # (characters between 0-9 and A-F) and are concatenated from two 8-character strings
    # just for ease of reading.
    key1 = "12305709" + "9BACD2F1"
    key2 = "21D0E319" + "BA56E604"
    key3 = "D1A253FF" + "ABC00213"

    # Initialize the Triple DES cipher with three keys
    des3Simple = DES3CipherSimple(key1, key2, key3)

    # Encrypt
    ciphertextBits = des3Simple.encrypt(plaintextBits)
    print(f"Encrypted bits: {ciphertextBits}")

    # Decrypt
    decryptedBits = des3Simple.decrypt(ciphertextBits)
    decryptedText = des_utility.bits2String(decryptedBits)
    print(f"Decrypted text: {decryptedText}")

    # Verify if decrypted text matches the original plaintext
    if decryptedText == plaintext:
        print("Decryption successful!")
    else:
        print("Decryption failed")

if __name__ == "__main__":
    main()