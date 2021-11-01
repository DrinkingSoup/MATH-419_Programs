import numpy as np
import matplotlib.pyplot as plt

def corrupt_code(byte, probability):
    '''
    Description
    -----------
    Corrupts the bits of a byte by a chance proportional to the probability

    Parameters
    ----------
    byte : Numpy Array
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
     
    #Iterate through bits in byte
    for bit in byte:
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

def short_to_redundant(short_byte_array, multiplier):
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
    if(multiplier < 0):
        raise ValueError("Multiplier cant be negative")

    #Place to store the new redundant array
    redundant_array = []

    #Iterate through every byte in the short byte array
    for byte in short_byte_array:
        redundant_entry = []

        #Combine a "multiplier" amount of byte entries into a single entry
        for i in range(multiplier):
            #Note: the numpy array needs to be converted
            #back into a regular list for the += operator to work
            redundant_entry += byte.tolist()
        
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
        #append the original byte to the short array
        short_array.append([x for x in redundant_byte[:8]])

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
    Numpy Matrix
        The "recieved" message as a byte array
    '''

    #apply the desired redundancy to the message
    mssg_array = short_to_redundant(str2bin(sentence), n_redundancy)

    #place to store "recieved" message
    new_mssg_array = []

    #Iterate through each byte in the message array
    for redundant_byte in mssg_array:
        #add a corrupted version of the byte to the new array
        new_mssg_array.append(corrupt_code(redundant_byte, corruption_probability).tolist())

    #return the new array as a numpy array
    return np.array(new_mssg_array)

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

def draw_histogram(data):
    plt.hist(data)
    plt.show()

def generate_dataset(original_mssg, dataset_size, n_redundancy, corruption_probability, robust=True):
    '''
    Description
    -----------
    Generate a byte array dataset from a message. This simulates a message being sent multiple
    times to multiple possible locations with a chance of corruption

    Parameters
    ----------
    original_mssg : String
        The original string that will generate the dataset
    dataset_size : Int
        The amount of elements in the dataset as a positive integer 
    n_redundancy : Int 
        A non-negaitve integer value multiplier
    corruption_probability : Float
        A decimal value from 0 to 1 that represents the probability
        of corruption (if desired)
    robust : Bool
        Choose whether or not to generate the hamming distances by byte
        or bit distances (default is true)
    
    Returns
    -------
    Numpy Matrix
        The dataset as a numpy matrix
    '''

    #raise an error if the size parameter is less than 1
    if dataset_size < 1:
        raise ValueError("Size of the dataset must be at least 1")
    
    #string as binary array
    mssg = str2bin(original_mssg)

    #place to store data
    data = []

    #generate an element "dataset_size" times
    for i in range(dataset_size):
        #calculate and append hamming
        if robust:
            data.append(byte_array_hamming_distance_robust(send_message(original_mssg, n_redundancy, corruption_probability), short_to_redundant(mssg, n_redundancy)))
        else:
            data.append(byte_array_hamming_distance(send_message(original_mssg, n_redundancy, corruption_probability), short_to_redundant(mssg, n_redundancy)))

    #return the dataset
    return np.array(data)


if __name__ == "__main__":
    
    char = char2byte("f")

    char_array1 = str2bin("abc123")

    char_array2 = str2bin("abc456")

    #print(bin2str(byte_array))
    #print(str2bin("abc123"))
    

    #print(byte2char(byte))
    #print(corrupt_code(byte, .5))
    #print(ord2eight_bit(54))
    #print(char_array)
    #print(send_message("abc123", 2, 0.6))
    
    data = generate_dataset("cheese pizza in my mouth now", 50, 1, .5, True)
    print(data)
    draw_histogram(data)
    
   


    