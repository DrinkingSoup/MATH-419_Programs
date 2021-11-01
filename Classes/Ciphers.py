from typing import Hashable
import numpy as np

class Ciphers:
    '''
    This class contains many tools to for use in encryption
    '''
    
    num2let = {
        0 : "A",
        1 : "B",
        2 : "C",
        3 : "D",
        4 : "E",
        5 : "F",
        6 : "G",
        7 : "H",
        8 : "I",
        9 : "J",
        10 : "K",
        11 : "L",
        12 : "M",
        13 : "N",
        14 : "O",
        15 : "P",
        16 : "Q",
        17 : "R",
        18 : "S",
        19 : "T",
        20 : "U",
        21 : "V",
        22 : "W",
        23 : "X",
        24 : "Y",
        25 : "Z",
        26 : " ",
        27 : ".",
        28 : ",",
        29 : ";"
    }

    let2num = {
        "A" : 0,
        "B" : 1,
        "C" : 2,
        "D" : 3,
        "E" : 4,
        "F" : 5,
        "G" : 6,
        "H" : 7,
        "I" : 8,
        "J" : 9,
        "K" : 10,
        "L" : 11,
        "M" : 12,
        "N" : 13,
        "O" : 14,
        "P" : 15,
        "Q" : 16,
        "R" : 17,
        "S" : 18,
        "T" : 19,
        "U" : 20,
        "V" : 21,
        "W" : 22,
        "X" : 23,
        "Y" : 24,
        "Z" : 25,
        " " : 26,
        "." : 27,
        "," : 28,
        ";" : 29
    }

    
    def __init__(self) -> None:
        self.HASH_LEN = len(self.num2let)

    def word2list(self,word):
        '''
        Resolves a list of integers from a string according to the dictionaries

        @param word: A string that is to be converted into a list of character ids
        '''
        return [self.let2num[x] for x in word.upper()]

    def list2word(self,num):
        '''
        Resolves a string from a list of integers according to the dictionaries

        @param num: A list of character ids that are to be converted into a string
        '''
        return "".join(self.num2let[x] for x in num)

    def shift_cipher(self, sentence, shift_val, character_flags=""):
        '''
        Encrypts plaintext using a shift cipher with flags that allow certain
        characters to be ignored if desired
        
        @param sentence: The plaintext that will be shifted
        @param shift_val: The amount of shift
        @param character_flags: A string of characters to be ignored e.i ";.,"
        '''
        #Storage for the numbers of the cipher
        cipher = []

        for i in self.word2list(sentence):
            if self.num2let[i] in list(character_flags.upper()):
                cipher.append(i)
            else:
                cipher.append((i + shift_val)%self.HASH_LEN)

        return self.list2word(cipher)

    def vigenere_cipher(self, sentence, keyword, character_flags=""):
        '''
        Encryptes plaintext using teh vigenere cipher algorithm
        using a keyword and optional characters to ignore.

        @param sentence: The plaintext that will be encrypted
        @param keyword: The keyword that will be used to encrypt the plaintext
        @param character_flags: A string of characters to be ignored e.i ";.,"
        '''
        key_char_queue = [self.let2num[keyword[x%len(keyword)].upper()] for x in range(len(sentence))]
        cipher = []

        for char_num,shift in zip(self.word2list(sentence), key_char_queue):
            if self.num2let[char_num] in list(character_flags.upper()):
                cipher.append(char_num)
            else:
                cipher.append((char_num + shift)%self.HASH_LEN)

        return self.list2word(cipher)
        
    def vigenere_keyword_inverse(self, keyword):
        '''
        Produces a keyword that decrypts a vingenere cipher given
        the keyword that was used to produce the cipher

        @param keyword: The keyword used to create the original cipher
        '''
        inverse_key = [self.HASH_LEN - self.let2num[x] for x in keyword.upper()]

        return self.list2word(inverse_key)

    def affine_cipher(self,sentence, coeff, offset):
        '''
        Produces an affine cipher based on a coefficient and shift offset

        @param sentence: The plaintext that will be encrypted
        @param coeff: The coefficient of the affine function
        @param offset: The shift offset of the affine function
        '''
        cipher = [((char_num * coeff) + offset)%self.HASH_LEN for char_num in self.word2list(sentence)]

        return self.list2word(cipher)

    #def permutation_cipher(self, sentence, keyword):

    def mod_inv(self,num, mod):
        for i in range(mod):
            if num * i%mod == 1:
                return i



    def inverse_affine_cipher(self, cipher, coeff, offset):
        new = []
        for i in self.word2list(cipher):
            coeff_inv = self.mod_inv(coeff, self.HASH_LEN)

            temp = i * coeff_inv - offset * coeff_inv
            new.append(temp%self.HASH_LEN)
        return self.list2word(new)
    
    def block_cipher(self, plaintext, dummy_char):
        if len(plaintext)%2 == 1:
            plaintext += dummy_char

        nums = self.word2list(plaintext)
        pairs = []

        while len(nums) != 0:
            pair = []

            pair.append(nums.pop(0))
            pair.append(nums.pop(0))

            pairs.append(pair)

        print(pairs)




if __name__ == "__main__":

    c = Ciphers()
    #print(word2list("WADASDWD"))
    #print(list2word([1,2,5,6,2,3]))

    #print(vigenere_cipher("Hello; Workd", "Wawdjkna"))
    #print(shift_cipher_naive("b,in.gu;;s", 2, "."))
    #print(vigenere_cipher("gum.bo", "lemon", "."))
    #print(vigenere_keyword_inverse("lemon"))
    #print(vigenere_cipher("RYY.OZ", "T SQR", "."))
    text = "howard hastily hoiseted his happy halloween harold now hovering high overhead his house"
    c.block_cipher("Hello", "X")


    

    

