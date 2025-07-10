# Ciucaru Andrei 10MF241

import math

class Vigenere2DCipher:
    # Private static numbers that represent the ASCII code limits of
    # allowed characters.
    # The range of allowed characters is between ASCII codes 32-126 (limits included),
    # which are the printable ASCII characters.
    __minAllowedAsciiCode: int = 32 # 'space' character
    __maxAllowedAsciiCode: int = 126 # '~' character
    __numberOfValues: int = __maxAllowedAsciiCode - __minAllowedAsciiCode

    # ASCII code of padding character, used to fill matrix if necesary
    __paddingAsciiCode: int = 0 # null character

    def __init__(self):
        print("Vigenere 2D cipher created")

    # Private method that verifies if the plain text contains only the allowed characters,
    # This function returns a boolean value:
    # - True if the text is OK
    # - False if the text has at least one dissallowed character
    def __isPlainTextValid(self, text: str) -> bool:
        # The character that will be extracted from the 'text' and verified if it's between
        # the ASCII code limits '__minAllowedAsciiCode' and '__maxAllowedAsciiCode'
        currentChar = 'a'
        currentCharAsciiCode: int = 0

        # For each character of the text to be verified
        for charIndex in range(len(text)):
            # Get the current character
            currentChar = text[charIndex]

            # Get the ASCII code of the current character
            currentCharAsciiCode: int = ord(currentChar)

            # Check if the current character ASCII code is outside the allowed ASCII codes
            if not (Vigenere2DCipher.__minAllowedAsciiCode <= currentCharAsciiCode <= Vigenere2DCipher.__maxAllowedAsciiCode or
                    currentCharAsciiCode == Vigenere2DCipher.__paddingAsciiCode):
                # Text contains at least one character out the allowed limits, so return imediately
                print("Text is not valid")
                return False
            
            # Else, if all characters are between allowed limits, we return True
            # meaning the text is OK
            return True
        
    # Private method that verifies if the password contains only the allowed characters,
    # This function returns a boolean value:
    # - True if the text is OK
    # - False if the text has at least one dissallowed character
    # This function is practically identical to the previous, with the exception that a 'null'
    # character is not allowed in passwords
    def __isPasswordValid(self, password: str) -> bool:
        # The character that will be extracted from the 'text' and verified if it's between
        # the ASCII code limits '__minAllowedAsciiCode' and '__maxAllowedAsciiCode'
        currentChar = 'a'
        currentCharAsciiCode: int = 0

        # For each character of the text to be verified
        for charIndex in range(len(password)):
            # Get the current character
            currentChar = password[charIndex]

            # Get the ASCII code of the current character
            currentCharAsciiCode: int = ord(currentChar)

            # Check if the current character ASCII code is outside the allowed ASCII codes
            if not (Vigenere2DCipher.__minAllowedAsciiCode <= currentCharAsciiCode <= Vigenere2DCipher.__maxAllowedAsciiCode):
                # Text contains at least one character out the allowed limits, so return imediately
                print("Text is not valid")
                return False
            
            # Else, if all characters are between allowed limits, we return True
            # meaning the text is OK
            return True
    
    # This helper method computes and returns the width (number of columns) and height (number of rows)
    # of a matrix in such a way that the number of elements in the matrix is equal or greater than the
    # provided number.
    # It is usefull for finding suitable dimensions for converting an array into a matrix.
    def __getMatrixSize(self, arrayLength: int) -> tuple[int, int]:
        matrixWidth: int = math.floor(math.sqrt(arrayLength))
        matrixHeight: int = math.ceil(arrayLength / matrixWidth)

        # print(arrayLength, matrixWidth, matrixHeight)

        return (matrixWidth, matrixHeight)
            
    # Helper method that converts a string (basically, a uni-dimensional array of characters) to a matrix
    # of characters (strings)
    def __getTextMatrix(self, text: str) -> list[list[str]]:
        textMatrix: list[list[str]] = []

        textLength: int = len(text)

        # Determine the nomber of rows that the matrix will have
        matrixWidth, matrixHeight = self.__getMatrixSize(len(text))

        # How many characters of the original text where already appended to the matrix
        numberOfAppendedChars: int = 0

        # The row of the current iteration that should be added to the matrix
        currentRow: list[str] = []
        for row in range(0, matrixHeight, 1):
            currentRow = [] # always reset current row every iteration

            # The row could be complete but also incomplete, so we check if the row is complete:

            # If the current row is complete (contains only characters from original text and does
            # not require padding characters)
            if (numberOfAppendedChars + matrixWidth <= textLength):
                currentRow = list(text[row * matrixWidth : (row + 1) * matrixWidth])
                numberOfAppendedChars += matrixWidth
            # If the current row is incomplete (partially contains characters from original text but also
            # requires some padding characters)
            else:
                # First, the current row will contain all remaining characters of the text
                currentRow: list[str] = list(text[row * matrixWidth : textLength])

                # Then, we find how many padding characters we need
                numberOfPaddingChars: int = matrixWidth - len(currentRow)

                # Create a string with the required padding characters, by repeating 'null' 'numberOfPaddingChars' times
                paddingCharacters: str = chr(Vigenere2DCipher.__paddingAsciiCode) * numberOfPaddingChars

                # Add the padding characters (as a list, not a string) to the current row list
                currentRow.extend(list(paddingCharacters))

                numberOfAppendedChars += matrixWidth - numberOfPaddingChars

            # Append the cuyrrent row to the matrix
            textMatrix.append(currentRow)

        return textMatrix

    # Method that encrypts a text (plainText) with a key and returns the encripted text.
    # This method can only encrypt a text that contains only valid characters.
    # The encryption key must also contain valid characters.
    # If the text to be encrypted or the key don't contain valid characters, the this method
    # will not encrypt the text and will return an empty string.
    def encrypt(self, plainText: str, key: str) -> list[list[str]]:
        # First, verify if the text to be encrypted contains only valid characters
        isPlainTextValid = self.__isPlainTextValid(plainText)

        # Secondly, verify if the key also contains only valid characters
        isKeyValid = self.__isPasswordValid(key)

        # If the plain text or key contain illegal characters, then return and exit
        if not isPlainTextValid or not isKeyValid:
            return None
        
        # At this point we know for sure both plain text and key contain only valid characters
        # and we can start encription

        plainTextMatrixWidth, plainTextMatrixHeight = self.__getMatrixSize(len(plainText))
        keyMatrixWidth, keyMatrixHeight = self.__getMatrixSize(len(key))

        plainTextMatrix: list[list[str]] = self.__getTextMatrix(plainText)
        keyMatrix: list[list[str]] = self.__getTextMatrix(key)

        # The final encripted text, with initial empty value
        cipherTextMatrix: list[list[str]] = []
        # The current iteration row, represents one element of 'cipherText'
        cipherTextRow: list[str] = []

        # The curent iteration's character of the plain text
        plainChar = ''

        # The current iteration ASCII code of the character of the text to be encripted.
        # The text's characters will have ASCII code between 32 ans 126:
        # 32 <= plain text character <= 126
        # This means that there are 95 possible values and if we count these values from zero,
        # as indexes, we find that, for the text character index (named 'plainCharIndex'),
        # the true value range is:
        # 0 <= plainCharIndex <= 94
        # So the 'plainCharIndex' will vary between 0 and 94 and the erncripted version of the
        # character should also vary between those limits (and be modulo truncated to not exceed 94)
        plainCharIndex = 0

        # The current iteration index of the encrypted version of the text's character.
        # This also varies between 0 and 94
        encryptedCharIndex = 0


        # The row and col index of the current character of the key matrix
        keyCharRow: int = 0
        keyCharCol: int = 0

        # The current iteration character of the key
        keyChar = '' 

        # The offset of the key's current character, which will be used
        # to offset (encrypt) the current iteration character of the original text
        # This offset is also between 0 and 94 limits:
        # 0 <= keyCharIndex <= 94
        keyCharIndex = 0

        # Traverse chars in the matrix of characters
        for row in range(plainTextMatrixHeight):
            # Reset the current row
            cipherTextRow = []

            for col in range(plainTextMatrixWidth):
                # Get the current character of the plain text
                plainChar = plainTextMatrix[row][col]

                # If the current character of the plain text is not a padding character, then we encrypt it
                if (ord(plainChar) != Vigenere2DCipher.__paddingAsciiCode):
                    # Determine the index of the current iteration character, this will be
                    # a number between 0 and 95
                    plainCharIndex = ord(plainChar) - 32

                    # Determine the row and col index of the current character of the key matrix
                    keyCharRow = row % keyMatrixHeight
                    keyCharCol = col % keyMatrixWidth

                    # Get the current character of the key
                    keyChar = keyMatrix[keyCharRow][keyCharCol]

                    # If the current character of the key is not a padding character
                    if (ord(keyChar) != Vigenere2DCipher.__paddingAsciiCode):
                        # Determine the offset that the key's character will induce to the original character
                        # The offset will be a number between 0 and 95
                        keyCharIndex = ord(keyChar) - 32
                    else:
                        keyCharIndex = 0 # no offset (no encryption)

                    # We offset the original (non-encrypted) character index by the index of the
                    # encription key's character. This encrypts the current index.
                    # The obtained index of the encrypted character might be larger than 94 (it varies
                    # between 0 and 2*94), so we also modulo truncate it by 94:
                    encryptedCharIndex = (plainCharIndex + keyCharIndex) % Vigenere2DCipher.__numberOfValues

                    # We append the encripted character to the encrypted version of the text.
                    # Because the 'textCurrentCharEncryptedIndex' is an index (between 0 and 95) and not
                    # an ASCII code (of expected range (32, 127)), we add 32 to make it an actual ASCII code
                    cipherTextRow.extend(chr(encryptedCharIndex + 32))

                    # print(f"enc iteration {index}: oc index: {plainCharIndex} k index: {keyCharIndex} ec index: {encryptedCharIndex} {cipherText}")
                else:
                    # Else, if the current plain text is a padding character, we leave it as it is
                    # but we still added to the final result matrix
                    cipherTextRow.extend(plainChar)
                
            cipherTextMatrix.append(cipherTextRow)

        print("Original matrix:")
        self.__printMatrix(plainTextMatrix)

        print("Key Matrix")
        self.__printMatrix(keyMatrix)

        print("Encrypted matrix:")
        self.__printMatrix(cipherTextMatrix)

        return cipherTextMatrix
    
    # Method that decrypts a text (encryptedText) with a key and returns the decripted text.
    # This method can dencrypts the text as a matrix.
    # The encryption key must contain only valid characters.
    # If the key doesn't contain valid characters, the this method will not decrypt the text
    # and will return an empty string.
    def decrypt(self, encryptedTextMatrix: list[list[str]], key: str) -> list[list[str]]:
        # First, verify if the key also contains only valid characters
        isKeyValid = self.__isPasswordValid(key)

        # If the key contains illegal characters, then return and exit
        if not isKeyValid:
            return None
        
        # At this point we know for sure both plain text and key contain only valid characters
        # and we can start encription

        # Determine the height of the encrypted matrix
        encryptedTextMatrixHeight = len(encryptedTextMatrix)

        # Determine the width of the encrypted matrix
        encryptedTextMatrixWidth = 0
        if (encryptedTextMatrixHeight > 0):
            encryptedTextMatrixWidth = len(encryptedTextMatrix[0])

        keyMatrixWidth, keyMatrixHeight = self.__getMatrixSize(len(key))

        keyMatrix: list[list[str]] = self.__getTextMatrix(key)

        # The final encripted text, with initial empty value
        plainTextMatrix: list[list[str]] = []
        # The current iteration row, represents one element of 'cipherText'
        plainTextRow: list[str] = []

        # The curent iteration's character of the plain text
        encryptedChar = ''

        # The current iteration ASCII code of the character of the text to be decripted.
        # The text's characters will have ASCII code between 32 ans 126:
        # 32 <= plain text character <= 126
        # This means that there are 95 possible values and if we count these values from zero,
        # as indexes, we find that, for the text character index (named 'encryptedCharIndex'),
        # the true value range is:
        # 0 <= encryptedCharIndex <= 94
        # So the 'encryptedCharIndex' will vary between 0 and 94 and the erncripted version of the
        # character should also vary between those limits (and be modulo truncated to not exceed 94)
        encryptedCharIndex = 0

        # The current iteration index of the encrypted version of the text's character.
        # This also varies between 0 and 94
        plainCharIndex = 0


        # The row and col index of the current character of the key matrix
        keyCharRow: int = 0
        keyCharCol: int = 0

        # The current iteration character of the key
        keyChar = '' 

        # The offset of the key's current character, which will be used
        # to offset (encrypt) the current iteration character of the original text
        # This offset is also between 0 and 94 limits:
        # 0 <= keyCharIndex <= 94
        keyCharIndex = 0

        # Traverse chars in the matrix of characters
        for row in range(encryptedTextMatrixHeight):
            # Always reset the current row at the begining of the iteration
            plainTextRow = []

            for col in range(encryptedTextMatrixWidth):
                # Get the current character of the plain text
                encryptedChar = encryptedTextMatrix[row][col]

                # If the current character of the plain text is not a padding character, then we decrypt it,
                # otherwise we leave it as it is
                if (ord(encryptedChar) != Vigenere2DCipher.__paddingAsciiCode):
                    # Determine the index of the current iteration character, this will be
                    # a number between 0 and 95
                    encryptedCharIndex = ord(encryptedChar) - 32

                    # Determine the row and col index of the current character of the key matrix
                    keyCharRow = row % keyMatrixHeight
                    keyCharCol = col % keyMatrixWidth

                    # Get the current character of the key
                    keyChar = keyMatrix[keyCharRow][keyCharCol]

                    # If the current character of the key is also not a padding character
                    if (ord(keyChar) != Vigenere2DCipher.__paddingAsciiCode):
                        # Determine the offset that the key's character will induce to the original character
                        # The offset will be a number between 0 and 95
                        keyCharIndex = ord(keyChar) - 32
                    else:
                        keyCharIndex = 0 # no offset (no encryption)

                    # We offset the original (encrypted) character index by the index of the
                    # encription key's character, but by subtraction, not by addition. This decrypts the current index.
                    # The obtained index of the decrypted character might be outside the (0,94) range (it varies
                    # between -94 and 94), so we also modulo truncate it by 94:
                    plainCharIndex = (encryptedCharIndex - keyCharIndex) % Vigenere2DCipher.__numberOfValues

                    # We append the decripted character to the decrypted matrix.
                    # Because the 'plainCharIndex' is an index (between 0 and 95) and not
                    # an ASCII code (of expected range (32, 127)), we add 32 to make it an actual ASCII code
                    plainTextRow.extend(chr(plainCharIndex + 32))

                    # print(f"enc iteration {index}: oc index: {plainCharIndex} k index: {keyCharIndex} ec index: {encryptedCharIndex} {cipherText}")
                else:
                    # Else, if the current plain text is a padding character, we leave it as it is
                    # but we still added to the final result matrix
                    plainTextRow.extend(encryptedChar)
                
            plainTextMatrix.append(plainTextRow)

        print("Decrypted matrix:")
        self.__printMatrix(plainTextMatrix)

        return plainTextMatrix
    
    # Method that prints a matrix of characters (strings) in an easy to read way
    def __printMatrix(self, textMatrix: list[list[str]]):
        matrixHeight: int = len(textMatrix)

        matrixWidth: int = 0
        if (matrixHeight > 0):
            matrixWidth = len(textMatrix[0])

        for row in range(matrixHeight):
            for col in range(matrixWidth):
                if (Vigenere2DCipher.__minAllowedAsciiCode <= ord(textMatrix[row][col]) <= Vigenere2DCipher.__maxAllowedAsciiCode):
                    print(textMatrix[row][col], end = " ")
                elif (ord(textMatrix[row][col]) == Vigenere2DCipher.__paddingAsciiCode):
                    print(textMatrix[row][col], end = "\\0")
            print("")
        
        print("")
    
    def testMatrixConversion(self, text):
        textMatrixWidth, textMatrixHeight = self.__getMatrixSize(len(text))
        textMatrix: list[str] = self.__getTextMatrix(text, textMatrixWidth)

        print(textMatrix)
    
def main():
    cypher = Vigenere2DCipher()
    key = '!  !'

    # print(cypher.encrypt("abcdefghijklmnop", "    "))
    encryptedMatrix: list[list[str]] = cypher.encrypt("abcdefghijklmnopqrs", key)

    decryptedMatrix: list[list[str]] = cypher.decrypt(encryptedMatrix, key)

if __name__ == "__main__":
    main()



