##----HOMEWORK 5 - ADAM UREMEK ----##

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
    ";" : 29}

HASH_LEN = len(num2let)

#my numpy matricies were not giving correct answers
#in numpy's linalg operations for some reason so i made my own.
#For all intents and purposes, just collapse and ignore this class.
class ModularMatrix:
    def __init__(self,mod, *args) -> None:
        self.__rows = [[y%mod for y in x] for x in args]
        self.__mod = mod

    def __add__(self, other):
        sum = []
        if self.size == other.size and self.modulus == other.modulus:
            for row1, row2 in zip(self.rows, other.rows):
                sum.append([a + b for a,b in zip(row1, row2)])
            return ModularMatrix(self.modulus, *sum)
        elif self.size != other.size:
            raise ValueError("Matricies must be of equal size and modulus to perfrom addition")
        else:
            raise ValueError("Matricies must be of equal modulus to perform opertaion")
            
    def __sub__(self, other):
        diff = []
        if self.size == other.size and self.modulus == other.modulus:
            for row1, row2 in zip(self.rows, other.rows):
                diff.append([a - b for a,b in zip(row1, row2)])
            return ModularMatrix(self.modulus, *diff)
        elif self.size != other.size:
            raise ValueError("Matricies must be of equal size to perfrom subtraction")
        else:
            raise ValueError("Matricies must be of equal modulus to perform opertaion")
    
    def __mul__(self, other):
        if type(other) == ModularMatrix:
            return self.__mat_mul(self, other)
        elif type(other) == int:
            return self.__scalar_mul(self, other)

    def __rmul__(self, other):
        if type(other) == int:
            return self.__scalar_mul(self, other)
            
    def __str__(self):
        str_list = [" ".join([str(y) for y in x]) for x in self.__rows]
        return "\n".join(str_list)
    
    def __repr__(self):
        str_list = [" ".join([str(y) for y in x]) for x in self.__rows]
        return "\n".join(str_list)
    
    def __mat_mul(self, m1, m2):
        if m1.size[1] == m2.size[0] and m1.modulus == m2.modulus:
            product = []
            for row1 in m1.rows:
                new_row = []
                for row2 in m2.transposed.rows:
                    new_row.append(sum([n1 * n2 for n1,n2 in zip(row1, row2)]))
                product.append(new_row)
            
            return ModularMatrix(self.modulus, *product)
        elif m1.size[1] != m2.size[0]:
            raise ValueError("Left matrix must have same number of columns as the right matrix does rows")
        else:
            raise ValueError("Matricies must be of the same modulus to perform operation")
    
    def __scalar_mul(self, m, s):
        scalar_product = []
        for row in m.rows:
            scalar_product.append([x * s for x in row])
        
        return ModularMatrix(self.modulus, *scalar_product)
    
    def __2x2_det(self, m):
        ad = m.rows[0][0] * m.rows[1][1]
        cb = m.rows[1][0] * m.rows[0][1]
        return (ad - cb)%self.modulus

    def __2x2_inv(self, m):
        inv_r1 = [m.rows[1][1],-1 * m.rows[0][1]]
        inv_r2 = [-1 * m.rows[1][0],m.rows[0][0]]
        inv_pre = ModularMatrix(self.modulus, inv_r1, inv_r2)

        return mod_inv(m.determinant, self.modulus) * inv_pre

    @property
    def size(self):
        return (len(self.__rows), len(self.__rows[0]))
    
    @property
    def rows(self):
        return self.__rows
    
    @property
    def cols(self):
        return ModularMatrix(self.modulus, self.transposed.rows)

    @property
    def modulus(self):
        return self.__mod
   
    @property
    def transposed(self):
        transposed = []
        for i in range(self.size[1]):
            row = []
            for j in range(self.size[0]):
                row.append(self.__rows[j][i])
            transposed.append(row)
        
        return ModularMatrix(self.modulus, *transposed)
    
    @property
    def determinant(self):
        if self.size[0] == self.size[1] == 2:
            return self.__2x2_det(self)

    @property
    def inverse(self):
        if self.size[0] == self.size[1] == 2:
            return self.__2x2_inv(self)






def word2list(word):
    '''
    Resolves a list of integers from a string according to the dictionaries

    @param word: A string that is to be converted into a list of character ids
    '''
    return [let2num[x] for x in word.upper()]

def list2word(num):
    '''
    Resolves a string from a list of integers according to the dictionaries

    @param num: A list of character ids that are to be converted into a string
    '''
    return "".join(num2let[x] for x in num)

def shift_cipher(sentence, shift_val, character_flags=""):
    '''
    Encrypts plaintext using a shift cipher with flags that allow certain
    characters to be ignored if desired
    
    @param sentence: The plaintext that will be shifted
    @param shift_val: The amount of shift
    @param character_flags: A string of characters to be ignored e.i ";.,"
    '''
    #Storage for the numbers of the cipher
    cipher = []

    for i in word2list(sentence):
        if num2let[i] in list(character_flags.upper()):
            cipher.append(i)
        else:
            cipher.append((i + shift_val)%HASH_LEN)

    return list2word(cipher)

def vigenere_cipher(sentence, keyword, character_flags=""):
    '''
    Encryptes plaintext using teh vigenere cipher algorithm
    using a keyword and optional characters to ignore.

    @param sentence: The plaintext that will be encrypted
    @param keyword: The keyword that will be used to encrypt the plaintext
    @param character_flags: A string of characters to be ignored e.i ";.,"
    '''
    key_char_queue = [let2num[keyword[x%len(keyword)].upper()] for x in range(len(sentence))]
    cipher = []

    for char_num,shift in zip(word2list(sentence), key_char_queue):
        if num2let[char_num] in list(character_flags.upper()):
            cipher.append(char_num)
        else:
            cipher.append((char_num + shift)%HASH_LEN)

    return list2word(cipher)

def vigenere_keyword_inverse(keyword):
    '''
    Produces a keyword that decrypts a vingenere cipher given
    the keyword that was used to produce the cipher

    @param keyword: The keyword used to create the original cipher
    '''
    inverse_key = [HASH_LEN - let2num[x] for x in keyword.upper()]

    return list2word(inverse_key)

def extended_euclidean_algorithm(a, b, twice=False):
    if a == 0:
        return (0, 1, b) if twice else b
    
    else:
        if twice:
            x, y, gcd  = extended_euclidean_algorithm(b % a, a, twice)
            return (y - (b // a) * x, x, gcd)
        else:
            return extended_euclidean_algorithm(b % a, a, twice)

def mod_inv(n, mod):
    x,y,gdc = extended_euclidean_algorithm(n,mod,True)

    if gdc != 1:
        return None
    else:
        return x%mod

def affine_cipher(sentence, coeff, offset):
    '''
    Produces an affine cipher based on a coefficient and shift offset

    @param sentence: The plaintext that will be encrypted
    @param coeff: The coefficient of the affine function
    @param offset: The shift offset of the affine function
    '''
    cipher = [((char_num * coeff) + offset)%27 for char_num in word2list(sentence)]

    return list2word(cipher)

def inverse_affine_cipher(cipher, coeff, offset):
    plaintext_list = []
    for i in word2list(cipher):
        coeff_inv = mod_inv(coeff, 27)

        temp = i * coeff_inv - offset * coeff_inv
        plaintext_list.append(temp%27)
    return list2word(plaintext_list)

def block_cipher(plaintext, coeff_mat, shift, dummy_char):
    if len(plaintext)%2 == 1:
        plaintext += dummy_char

    nums = word2list(plaintext)
    pairs = []

    while len(nums) != 0:
        pair = []

        pair.append(nums.pop(0))
        pair.append(nums.pop(0))

        pairs.append(pair)

    new = []

    for pair in pairs:
        new += [x for x in (ModularMatrix(coeff_mat.modulus, pair) * coeff_mat + shift).rows[0]]

    
    return list2word(new)

def inverse_block_cipher(cipher, coeff_mat, shift):
    nums = word2list(cipher)
    pairs = []

    while len(nums) != 0:
        pair = []

        pair.append(nums.pop(0))
        pair.append(nums.pop(0))

        pairs.append(pair)

    new = []
    for pair in pairs:
        new += [x for x in (ModularMatrix(27, pair) * coeff_mat.inverse - shift * coeff_mat.inverse).rows[0]]

    
    return list2word(new)

    
if __name__ == "__main__":
    plain_text = "howard hastily hoisted his happy halloween harold now hovering high overhead his house"
    

    #----------Q1----------#
    print("----------Q1----------")

    #Defined above as word2list() and list2word()
    test1 = word2list("stinky")
    print(test1)
    print(list2word(test1))

    print("----------------------\n")
    #----------Q2----------#
    print("----------Q2----------")

    #Defined above as shift_cipher()
    print("Shift Cipher: " + shift_cipher("sTi.nK", 4, ";,."))

    print("----------------------\n")

    #----------Q3----------#
    print("----------Q3----------")

    #Defined above as vigenere_cipher()
    #Q3.a
    print("Cipher: " + vigenere_cipher(plain_text, "skeleton"))

    #Q3.b
    #defined above as vigenere_keyword_inverse()
    key_inv = vigenere_keyword_inverse("skeleton")
    vig_cipher = vigenere_cipher(plain_text, "skeleton")
    print("Inverse Key: " + key_inv)
    print("Plaintext: " + vigenere_cipher(vig_cipher, key_inv))
    

    print("----------------------\n")

    #----------Q4----------#
    print("----------Q4----------")

    #defined above as extended_euclidean_algortihm()
    print("Without linear combo: "+ str(extended_euclidean_algorithm(106, 6)))
    print("With linear combo: "+ str(extended_euclidean_algorithm(106, 6, True)))

    print("----------------------\n")

    #----------Q5----------#
    print("----------Q5----------")

    #defined above as affine_cipher()
    #Q5.a
    print("Cipher: " + affine_cipher(plain_text, 5, 3))

    #Q5.b
    #The only values that are approrpiate for the multiplication coeff.
    #are ones that have inverses modulo n. In other words: GDC(coeff, n) = 1

    #Q5.c
    #defined above as inverse_affine_cipher()
    cipher = affine_cipher(plain_text, 5, 3)
    print("Plaintext: " + inverse_affine_cipher(cipher, 5, 3))

    print("----------------------\n")

    #----------Q6----------#
    print("----------Q6----------")

    #defined above as block_cipher()
    #Q6.a
    coeff_mat = ModularMatrix(27, [2,5], [11,7])
    shift_mat = ModularMatrix(27, [4,9])
    cipher = block_cipher(plain_text, coeff_mat, shift_mat, "x")
    print("Cipher text: " + cipher)
    print()

    #Q6.b
    affine_coeff = ModularMatrix(27, [2,0],[0,2])
    affine_shift  = ModularMatrix(27, [1,1])
    vig_coeff = ModularMatrix(30, [1, 0], [0,1])
    vig_shift = ModularMatrix(30, [2, 5])

    shift_coeff = ModularMatrix(30, [1,0], [0,1])
    shift_shift = ModularMatrix(30, [2,2])

    print("Affine cipher: " + affine_cipher(plain_text, 2, 1))
    print("Affine block equivalent: " + block_cipher(plain_text, affine_coeff, affine_shift, "x"))
    print()
    print("Vigenere cipher: " + vigenere_cipher(plain_text, "cf"))
    print("Vigenere block equivalent: " + block_cipher(plain_text, vig_coeff, vig_shift, "x"))
    print()
    print("Shift cipher: " + shift_cipher(plain_text, 2))
    print("Shift block equlivalent: " + block_cipher(plain_text, shift_coeff, shift_shift, "x"))
    print()

    #The most important condition for all of the block ciphers is that thier coefficient matrix MUST 
    #be invertible, otherwise the cipher would be useless.
    #For an affine cipher, the coeff matrix must be some scalar times the identity 
    #and the shift matrix must be some vector where all of the entries are the same.
    #For a vigenere cipher, the coeff matrix must be the identity matrix and the 
    #shift matrix must be a vector with entires being equvalent to integer representation of characters.
    #Finally, for a shift cipher, the coeff matirx must be the identity matrix and the shift matrix must be
    #a vector where all entries are the same.

    #Q6.c
    #If the 2x2 matrix M mod n has a determinant that is invertible mod n, then M is invertile.
    #That is, if GDC(det(M), n) = 1, then the matrix has an inverse mod n.

    #Q6.d
    #defined above as inverse_block_cipher()
    print("Plaintext: " + inverse_block_cipher(cipher,coeff_mat, shift_mat))
    

    print("----------------------\n")