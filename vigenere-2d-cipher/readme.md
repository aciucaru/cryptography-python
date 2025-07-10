# 2D version of Vigenere cipher

Features:
* allows any printable ASCII character to be used both for text and for key (the printable ASCII codes are between 32 and 126, limits included)
* encrypts and decrypts using the Vigenere cipher but in 2 dimensions, converting both the text and the key to matrices

### How does it wok
First of  all, both the text and the key must be converted from a string to matrices. In order to do this we use two helper methods:
* __getMatrixSize(self, arrayLength: int) -> tuple[int, int]: computes and returns the width (number of columns) and height (number of rows) of a matrix in such a way that the number of elements in the matrix is equal or greater than the provided number
* __getTextMatrix(self, text: str) -> list: generates a matrix of characters (strings) from a string where the dimesion of the generated matrix is determined by the result of __getMatrixSize() method

The encryption is done inside the encrypt(self, plainText: str, key: str) public method. It work in the following way:
1. this method converts the plain text and key to matrices
2. for each element (character) of the plain text matrix, it computes it's ASCII code with the help of the ord() Python function and then subtract 32 to make that index start from 0 (because the allowed characters start from 32. not 0). We need the codes to start from 0 because we also do modulo division with the % operator and the % operator does not give predictable results if the operand does not start from 0
3. we determine the corresponding key row and key column corresponding to the plain text matrix's current row and column
4. we compute the ASCII code of the current key character and also subtract 32 from it, so it starts at 0, this is the key offset that will be applied to the character of plain text matrix
5. we use the key offset to offset the ASCII code of the plain text character, by adding them togheter
6. we add the current character to a row, wich is a list of strings, by usind the extend() method
7. we append the current row to the matrix, by ussing the append() method
8. in case the computed matrix width and height result in more characters than the original text, the last row will be padded with the 'null' character (ASCII code 0) and such character will be ignored for encryption

For decryption we use exactly the same apropach as for encryption, with the exception that we subtract the ASCII code of the key from the ASCII code of the chracters of the encrypted matrix. The text to be decrypted is passed to the decrypt() method as a matrix (list[list[str]]) not as a string.