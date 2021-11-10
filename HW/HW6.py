#--HW6--#
import numpy as np
import matplotlib.pyplot as plt

def corrupt_code(bit_list, probability):
    '''
    Description
    -----------
    Corrupts the bits of a byte by a chance proportional to the probability

    Parameters
    ----------
    bit_list : Numpy Array
        A list representation of a byte [ORIENTED FROM RIGHT TO LEFT] to be corrupted
    probability : Float
        A decimal value from 0 to 1 that represents the probability
        of corruption
    
    Returns
    -------
    Numpy Array
        A list representation of a byte [ORIENTED FROM RIGHT TO LEFT]
    '''
    new_byte = []
     
    #Iterate through bits in bit_lsit
    for bit in bit_list:
        #Generate a random decimal number from 0 - 1
        if np.random.uniform(0,1) < probability:
            #if the generated number is less than the probability, corrupt the bit
            new_byte.append(1-bit)
        else:
            #otherwise leave bit unchanged
            new_byte.append(bit)

    #return new "corrupted" byte as numpy array / vector
    return np.array(new_byte)

def eight_bit2ord(byte):
    '''
    Description
    -----------
    Converts a byte to an ordinal value

    Parameters
    ----------
    byte : Numpy Array
        A list representaion of a byte [ORIENTED FROM RIGHT TO LEFT]
    
    Returns
    -------
    Int
        The integer representation of the byte
    '''
    #Variable to store integer
    ord = 0

    #Generate a list of powers of 2 from 128 down to 1
    eight_bit = [pow(2,x) for x in range(7, -1, -1)]

    #Iterate through every bit and base and add 
    #thier product to the ordinal variable
    for bit, base in zip(byte, eight_bit):
        ord += base * bit

    #return the ordinal
    return ord

def ord2eight_bit(ord):
    '''
    Description
    -----------
    Converts an ordinal value into a byte

    Parameters
    ----------
    ord : Int
        The ordinal value to be converted into a byte
    
    Returns
    -------
    Numpy Array
        A list representation of a byte [ORIENTED FROM RIGHT TO LEFT]
    '''
    
    #Generate list of bits
    byte = [int(digit) for digit in bin(ord)[2:].zfill(8)]

    #return byte as numpy array / vector
    return np.array(byte)

def byte2char(byte):
    '''
    Description
    -----------
    Converts a byte to an ASCII character

    Parameters
    ----------
    byte : Numpy Array
        A list representation of a byte [ORIENTED FROM RIGHT TO LEFT]

    Returns
    -------
    String
        A character string
    '''

    #Return the character
    return chr(eight_bit2ord(byte))

def char2byte(char):
    '''
    Description
    -----------
    Converts a char to a byte

    Parameters
    ----------
    char : String
        The character string to be converted into a byte

    Returns
    -------
    Numpy Array
        A list representation of a byte [ORIENTED FROM RIGHT TO LEFT]
    '''

    #Return the byte
    return ord2eight_bit(ord(char))

def bin2str(byte_array):
    '''
    Description
    -----------
    Converts a byte array into a string

    Parameters
    ----------
    byte_array : Numpy Matrix
        A numpy (2D) array of bytes, AKA a numpy matrix

    Returns
    -------
    String
        The combined character representation of the byte array
    '''

    #Return the string
    return "".join([byte2char(x) for x in byte_array])

def str2bin(str):
    '''
    Description
    -----------
    Converts a string into a byte array

    Parameters
    ----------
    str : String
        The string of characters (a sentence) to be converted into
        a byte array
    
    Returns
    -------
    Numpy Matrix
        A numpy (2D) array of bytes, AKA a numpy matrix
    '''

    #Return the byte matrix / 2D list
    return np.array([char2byte(x) for x in list(str)])

def byte_array_to_matrix(byte_array):
    '''
    Description
    -----------
    A quality of life method that returns a nice readable string representation
    of a byte array

    Parameters
    ----------
    byte_array : Numpy Matrix
        A numpy (2D) array of bytes, AKA a numpy matrix
    
    Returns
    -------
    String
        A neat string representation of a byte array
    '''

    #place to store matrix contents
    matrix = ""

    #Iterate through byte array and format the list as a string
    for byte in byte_array:
        matrix += " ".join([str(x) for x in byte]) + "\n"

    #return the matrix string
    return matrix

def short_to_redundant(short_byte_array, multiplier, parity=False):
    '''
    Description
    -----------
    Takes a byte array with n bit bytes and applies redundnacy to each byte to
    make them "multiplier" times longer

    Parameters
    ----------
    short_byte_array : Numpy Matrix
        A numpy (2D) array of bytes, AKA a numpy matrix
    multiplier : Int
        A non-negaitve integer value multiplier
    
    Returns
    -------
    Numpy Matrix
        A redundant numpy (2D) array of bytes, AKA a numpy matrix
    '''

    #Raise an error if the multiplier is negative
    if multiplier < 0:
        raise ValueError("Multiplier cant be negative")
    if multiplier%2 == 0:
        raise ValueError("Multiplier cant be even")

    #Place to store the new redundant array
    redundant_array = []

    #Iterate through every byte in the short byte array
    for byte in short_byte_array.tolist():
        redundant_entry = []

        #add parity bit if needed
        if parity:
            byte.insert(0,0)
        #Iterate through every bit in the byte
        for bit in byte:
            redundant_entry.append([bit for x in range(multiplier)])
        
        #add the redundant entry to the redundant array
        redundant_array.append(redundant_entry)
    
    #return the redundant array as a numpy array
    return np.array(redundant_array)

def redundant_to_short(redundant_byte_array):
    '''
    Description
    -----------
    Converts a redundant byte array into its original short array

    Parameters
    ----------
    redundant_byte_array : Numpy Matrix
        A numpy (2D) array of bytes, AKA a numpy matrix
    
    Returns
    -------
    Numpy Matrix
        The short byte array
    '''

    #place to store new short
    short_array = []

    #Iterate through each redundant byte in the byte array
    for redundant_byte in redundant_byte_array:
        byte = []
        #Iterate through each redundant bit and convert them back to 
        #single bit
        for redundant_bit in redundant_byte:
            one_count = 0
            zero_count = 0

            for bit_i, bit_j in zip(redundant_bit,redundant_bit):
                one_count += 1 if bit_i == 1 else 0
                zero_count += 1 if bit_j == 0 else 0
            
            byte.append(1 if one_count > zero_count else 0)
        short_array.append(byte)

    #return the short array as a numpy array
    return np.array(short_array)

def send_message(sentence, n_redundancy=1, corruption_probability=0):
    '''
    Description
    -----------
    Simulates sending a message over some medium that has a chance of 
    corrupting the message, with the option of customizing the byte array's
    redundancy

    Parameters
    ----------
    sentence : String
        The message to be simulated being sent
    n_redundancy : Int
        The redundancy multiplier (if desired)
    corruption_probability : Float
        A decimal value from 0 to 1 that represents the probability
        of corruption (if desired)

    Returns
    -------
    String
        The "recieved" message as a string
    '''

    #apply the desired redundancy to the message
    mssg_array = short_to_redundant(str2bin(sentence), n_redundancy)

    #place to store "recieved" message
    corrupt_byte_array = []

    #Iterate through each byte in the message array
    for redundant_byte in mssg_array:
        #add a corrupted version of the byte to the new array
        corrupt_byte = []
        for redundant_bit in redundant_byte:
            corrupt_byte.append(corrupt_code(redundant_bit, corruption_probability).tolist())
        corrupt_byte_array.append(corrupt_byte)

    #return the new array as a string
    return bin2str(redundant_to_short(corrupt_byte_array))

def send_message2(sentence, n_redundancy=1, corruption_probability=0, parity=False):
    #apply the desired redundancy to the message
    mssg_array = short_to_redundant(str2bin(sentence), n_redundancy, parity)

    #place to store "recieved" message
    corrupt_byte_array = []

    #Iterate through each byte in the message array
    for redundant_byte in mssg_array:
        #add a corrupted version of the byte to the new array
        corrupt_byte = []
        for redundant_bit in redundant_byte:
            corrupt_byte.append(corrupt_code(redundant_bit, corruption_probability).tolist())
        corrupt_byte_array.append(corrupt_byte)

    return redundant_to_short(corrupt_byte_array)

def string_hamming_distance(str1, str2):
    '''
    Description
    -----------
    Compute the hamming distance between two strings

    Parameters
    ----------
    str1 : String
        The starting string
    str2 : String
        The ending string
    
    Returns
    -------
    Int
        The hamming distance between the two strings
    '''

    #raise an error if the strings are different sizes
    if len(str1) != len(str2):
        raise ValueError("str1 must be the same size as str2")

    #place to store distance
    distance = 0

    #iterate through each character in both strings
    for char1, char2 in zip(str1, str2):
        #increment the distance by 1 if the two characters are 
        #not the same
        distance += 1 if char1 != char2 else 0

    #return the distance
    return distance

def byte_hamming_distance(byte1,byte2):
    '''
    Description
    -----------
    Compute the hamming distance between two bytes

    Parameters
    ----------
    str1 : Numpy Array
        The starting byte [ORIENTED FROM RIGHT TO LEFT]
    str2 : Numpy Array
        The ending byte [ORIENTED FROM RIGHT TO LEFT]
    
    Returns
    -------
    Int
        The hamming distance between the two bytes
    '''

    #raise an error if the two bytes are not of equal size
    if len(byte1) != len(byte2):
        raise ValueError("The two bytes must be of equal size")

    #place to store distance
    distance = 0

    #iterate through each bit in both bytes
    for bit1, bit2 in zip(byte1, byte2):
        #increment the distance by 1 if the two bits are
        #not the same
        distance += 1 if bit1 != bit2 else 0

    #return the distance
    return distance

def byte_array_hamming_distance(byte_arr1, byte_arr2):
    '''
    Description
    -----------
    Compute the hamming distance between two bytes arrays

    Parameters
    ----------
    str1 : Numpy Matrix
        The starting byte array
    str2 : Numpy Matrix
        The ending byte array
    
    Returns
    -------
    Int
        The hamming distance between the two bytes arrays
    '''

    #raise an error if the matricies are not of equal size
    if(len(byte_arr1) != len(byte_arr2)):
        raise ValueError("The size of both matricies are not equal")

    #place to store distance
    distance = 0

    #iterate through every byte in each byte array
    for byte1, byte2 in zip(byte_arr1, byte_arr2):
        #if the bytes are equal, increment 
        distance += 1 if byte1.tolist() != byte2.tolist() else 0

    #return the distance
    return distance

def byte_array_hamming_distance_robust(byte_arr1, byte_arr2):
    '''
    Description
    -----------
    Compute the hamming distance between two bytes arrays' bits rather
    than the bytes themselves

    Parameters
    ----------
    str1 : Numpy Matrix
        The starting byte array
    str2 : Numpy Matrix
        The ending byte array
    
    Returns
    -------
    Int
        The hamming distance between the two bytes arrays's bits
    '''
    #raise an error if the matricies are not of equal size
    if(len(byte_arr1) != len(byte_arr2)):
        raise ValueError("The size of both matricies are not equal")
    
    #place to store distance
    distance = 0

    #iterate through every byte in each byte array
    for byte1, byte2 in zip(byte_arr1, byte_arr2):
        #increament the distance by the byte hamming distance of each
        #pair of bytes
        distance += byte_hamming_distance(byte1, byte2)
    
    #return distance
    return distance

def draw_histogram(data, title):
    plt.title(title)
    plt.hist(data)
    plt.show()

def generate_sums(corr_prob, trials):
    data = []
    for i in range(trials):
        sum = 0
        for bit in corrupt_code([0,0,0,0,0,0,0,0], corr_prob):
            sum += bit
        data.append(sum)

    return data

def generate_ham(sentence,n_redundancy,corr_prob, trials):
    data = []
    for i in range(trials):
        corr_msg = send_message(sentence, n_redundancy, corr_prob)
        data.append(string_hamming_distance(sentence, corr_msg))
    return data

def generate_ham2(sentence,n_redundancy,corr_prob, trials):
    single_errors = []
    double_errors = []
    for i in range(trials):
        corr_msg = send_message2(sentence, n_redundancy, corr_prob)
        total_single_error = 0
        total_double_error = 0
        for a,b in zip(corr_msg, str2bin(sentence)):
            if byte_hamming_distance(a,b) == 1:
                total_single_error += 1
            elif byte_hamming_distance(a,b) == 2:
                total_double_error += 1

        single_errors.append(total_single_error)
        double_errors.append(total_double_error)

    return single_errors, double_errors

def generate_ham3(sentence,n_redundancy, corr_prob, trials):
    single_errors = []
    double_errors = []
    predicted_singles = []
    predicted_doubles = []
    false_positives = 0
    for i in range(trials):
        corr_msg = send_message2(sentence, n_redundancy, corr_prob, parity=True)
        total_single_error = 0
        total_double_error = 0
        pred_single = 0
        pred_double = 0
        for a,b in zip(corr_msg.tolist(), str2bin(sentence)):
            if a.pop(0) == 1:
                if byte_hamming_distance(a,b) == 1:
                    pred_single += 1
                elif byte_hamming_distance(a,b) == 2:
                    pred_double += 1
                elif byte_hamming_distance(a,b) == 0:
                    false_positives += 1
            if byte_hamming_distance(a,b) == 1:
                total_single_error += 1
            elif byte_hamming_distance(a,b) == 2:
                total_double_error += 1

        single_errors.append(total_single_error)
        double_errors.append(total_double_error)
        predicted_singles.append(pred_single)
        predicted_doubles.append(pred_double)

    return single_errors, double_errors, predicted_singles, predicted_doubles, false_positives

def sums(corr_prob, trials):
    sum_list = [0,0,0,0,0,0,0,0,0,0]

    for i in range(trials):
        sum = 0 
        for i in [x for x in corrupt_code([0,0,0,0,0,0,0,0], corr_prob)]:
            sum += 1 if i == 1 else 0
        sum_list[sum] += 1
    return sum_list

if __name__ == "__main__":
    #Declaration of cetain varaibles
    sentence = "Talat the tragic turk ate Turkish turkey in Turkmenistan."

    #-----Q1------#
    print("-----Q1------")
    #1.a
    #Defined above as byte2char

    #1.b
    #Defined above as char2byte

    #1.c
    #Defined above as bin2str and str2bin

    #1.d 
    #Defined above as byte_array_to_matrix()
    
    #1.e
    enc = str2bin(sentence)
    dec = bin2str(enc)
    print("Encoding: \n" + byte_array_to_matrix(enc))
    print("Decoding: " + dec)
    print("-------------")

    #-----Q2------#
    print("-----Q2------")
    #2.a
    #i, ii, iii
    data = [generate_sums(0.04,10),generate_sums(0.04,100),generate_sums(0.04,1000)]
    for set in data:
        draw_histogram(set, "2.a")
        pass
    
    #2.b
    data = generate_sums(0.15,1000)
    draw_histogram(data, "2.b")

    #2.c
    data = generate_sums(0.5,1000)
    draw_histogram(data, "2.c")

    #2.d
    print("unique bytes")
    print("p=0.04:")
    print([i / j for i,j in zip(sums(0.04, 1000), [1,8,28,56,70,56,28,8,1])])
    print("p=0.15:")
    print([i / j for i,j in zip(sums(0.15, 1000), [1,8,28,56,70,56,28,8,1])])
    print("p=0.5:")
    print([i / j for i,j in zip(sums(0.5, 1000), [1,8,28,56,70,56,28,8,1])])

    print("-------------")

    #-----Q3------#
    #WARNING: this takes a long time to calculate :/#
    print("-----Q3------")
    #3.a
    #Defined above as short_to_redundant()

    #3.b
    #Defined above as redundant_to_short()

    #3.c 
    #Defined above as string_hamming_distance(),
    #byte_hamming_distance(), byte_array_hamming_distance(),
    #and byte_array_hamming_distance_robust()

    #3.d
    data = [generate_ham(sentence, 1, 0.15, 1000),generate_ham(sentence, 3, 0.15, 1000),generate_ham(sentence, 5, 0.15, 1000)]
    for set in data:
        draw_histogram(set, "3.d")
        pass
    
    #3.e
    data = [generate_ham2(sentence, 1, 0.15, 1000),generate_ham2(sentence, 3, 0.15, 1000),generate_ham2(sentence, 5, 0.15, 1000)]
    for set in data:
        draw_histogram(set[0], "3.e single")
        draw_histogram(set[1], "3.e double")
        pass
    
    #The change frequencies and amount of errors was more noticible in 3.e than 3.d

    #3.f
    data = [generate_ham3(sentence, 1, 0.15, 1000),generate_ham3(sentence, 3, 0.15, 1000),generate_ham3(sentence, 5, 0.15, 1000)]
    for set in data:
        #raw_histogram(set[0], "3.e single")
        draw_histogram(set[1], "3.e double")
        single = 0
        for x in set[0]:
            single += x
        pred_single = 0
        for x in set[2]:
            pred_single += x
        double = 0
        for x in set[1]:
           double += x
        pred_double = 0
        for x in set[3]:
            pred_double += x
        
        print(f"{pred_single} single errors were detected out of the {single}")
        print(f"{pred_double} double errors were detected out of the {double}")
        print(f"{set[4]} false positives were detected")
        print("\n")
        pass
    print("-------------")