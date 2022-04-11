#!/usr/local/opt/python@3.10/bin/python3

# Vigenere cipher encoder/decoder.
# github.com/flightcode
# 2022
# USAGE: 
#   python3 vigenere.py 
#       -m (e|encrypt, d|decrypt, i|interactive) 
#       [-f <filename> (required if -m not i|interactive)]
#       [-k <key> (required if -m e|encrypt)]

import sys # For CLI rguments
import getopt # Parses CLI arguments
import itertools # Code-efficient iterators
import string

def main(): # Welcome message and run menu
    print("--- VIGENERE CIPHER ----")
    print("--- FLIGHTCODE 2022 ----")

    fileName = "" # File to parse
    mode = "" # Mode (interactive is for testing or if user wants a menu)
    key = "" # If applicable, if not provided for decode, will attempt to crack. Required for encode.

    try: # Attempt to parse arguments (Strip first argument (Command))
        opts, args = getopt.getopt(sys.argv[1:], "m:f:k:")
    except:
        errorMessage("Unable to parse arguments!")

    for opt, arg in opts: # Assign from arguments 
        if opt in ['-f']:
            fileName = arg
        elif opt in ['-m']:
            mode = arg
        elif opt in ['-k']:
            key = arg

    if mode == "interactive" or mode == "i":
        menu()
    elif mode == "encrypt" or mode == "e" or mode == "decrypt" or mode == "d":
        if fileName != "":
            file = open(fileName, "r") # Open file in read mode
            text = file.read() # Read file contents to string
            file.close() # Close file
            if mode == "encrypt" or mode == "e":
                if key != "":
                    print("--- START ENCRYPTION ---")
                    encrypted = encrypt(text,key) # Encrypt string `decrypted` with key `key`
                    file = open(f"{fileName}.out", "w") # Open file in write mode
                    file.write(encrypted) # Write encrypted string to file contents
                    file.close() # Close file
                    print(f"--- OUTPUT to '{fileName}.out' ---")
                    print("--- FINISH ENCRYPTION ---")
                else:
                    return errorMessage("Key not specified!")
            elif mode == "decrypt" or mode == "d":
                print("--- START DECRYPTION ---")
                key = solve(text) # Find correct key
                print("--- KEY SOLVED ---")
                decrypted = decrypt(text, key)
                file = open(f"{fileName}.out", "w") # Open file in write mode
                file.write(decrypted) # Write decrypted string to file contents
                file.close() # Close file
                print("--- FINISH DECRYPTION ---")
        else:
            return errorMessage("File not specified!")
    else:
        return errorMessage("Invalid mode specified!")

def encrypt(decrypted, key): # Encrypt string with given key    
    # Encrypts using iterated-key method, where for each character in string, 
    # character is encrypted by nth character in string (modulo key length. 
    # This simulates a key of same length as string, but is more memory efficient)

    key = key.upper()
    lowerStart = ord('a') # Start shift for 'a' in lowercase
    upperStart = ord('A') # Start shift for 'A' in uppercase
    encrypted = ""

    i = 0
    for c in decrypted:
        if c.isalpha():
            if c.isupper(): # Uppercase shift
                start = upperStart
            else: # Lowercase shift
                start = lowerStart

            cPos = ord(c) - start # Get position of char
            shift = ord(key[i % len(key)]) - upperStart # Get shift amount based on keyPos (Key is in uppercase)
            cNewPos = (cPos + shift) % 26 # Get position of shifted char
            
            encrypted += chr(cNewPos + start) # Add character to encrypted string
            i += 1
        else: # If not alphanumeric
            encrypted += c
    return encrypted

def decrypt(encrypted, key): # Decrypt string with given key
    # Decrypts using iterated-key method, where for each character in string, 
    # character is decrypted by nth character in string (modulo key length. 
    # This simulates a key of same length as string, but is more memory efficient)
    
    key = key.upper()
    lowerStart = ord('a') # Start shift for 'a' in lowercase
    upperStart = ord('A') # Start shift for 'A' in uppercase
    decrypted = ""

    i = 0
    for c in encrypted:
        if c.isalpha():
            if c.isupper(): # Uppercase shift
                start = upperStart
            else: # Lowercase shift
                start = lowerStart

            cPos = ord(c) - start # Get position of char
            shift = ord(key[i % len(key)]) - upperStart # Get reverseshift amount based on keyPos (Key is in uppercase)
            cNewPos = (cPos - shift) % 26 # Get position of shifted char
            
            decrypted += chr(cNewPos + start) # Add character to decrypted string
            i += 1
        else: # If not alphanumeric
            decrypted += c
    return decrypted

def solve(encrypted): # Decrypt string without key, returning best match
    # Initially used itertools.product to get all possible key combinations 
    # of length `l` (from 1 to length of message). However after research,
    # I discovered that by decrypting every nth letter (based on key length),
    # and then testing the frequency, I could run tests much quicker, as a
    # smaller dataset was being used, not repeating over the same char in the
    # same index.
    #
    # This reduced complexity from O(26^key_length) to O(26*key_length).

    encryptedTrimmed = [c for c in encrypted.upper() if c in string.ascii_uppercase]
    keys = []
    for l in range(len(encrypted)): # Try all possible key lengths
        l += 1
        keyAccuracy = 0
        key = ""
        for i in range(l): # Iterate through nth letter of key length
            affectedLetters = "".join(itertools.islice(encryptedTrimmed, i, None, l)) # Get every nth letter from `encrypted`
            shifts = []
            for c in string.ascii_uppercase: # Try all possible characters for nth letter
                decrypted = decrypt(affectedLetters, c) # Get decrypted string from possible key
                accuracy = freqTest(decrypted) # Get accuracy of decrypted string
                shifts.append((accuracy, c)) # Add possible shift to array
            bestChar = min(shifts, key=lambda x: x[0])
            keyAccuracy += (bestChar[0] / l) # Add char accuracy to key accuracy, divide by key_length avoids biasing for smaller keys
            key += bestChar[1]
        keys.append((keyAccuracy,key))
        # print(f"Best key at length {l} = {(keyAccuracy,key)}") # DEBUGGING
       
        # OLD USING itertools.product
        #
        # print(f"Trying key length {l}...")
        # keys = itertools.product(string.ascii_uppercase, repeat = l) # Get all possible key combinations of length `l`
        # shifts = []
        # for k in keys: # Try all possible keys of length `l`
        #     key = "".join(k)
        #     decrypted = decrypt(encrypted, key) # Get decrypted string from possible key
        #     accuracy = freqTest(decrypted) # Get accuracy of decrypted string
        #     shifts.append((accuracy, key)) # Add possible shift to array
        # bestShifts.append(min(shifts, key=lambda x: x[0])) # Add best key combination from this key length to `bestShifts` (Sorted by `accuracy` value of tuple)
        # print(f"Best key at length {l} = {min(shifts, key=lambda x: x[0])}")

    bestKey = min(keys, key=lambda x: x[0]) # Return most accurate key from `bestKeys` at all key lengths
    # print(f"Best key overall = {bestKey}") # DEBUGGING
    return bestKey[1] # Return `bestKey`

def freqTest(message): # Test frequency of string against English language alphabet frequencies using Chi-Squared Test (0 is most accurate)
    # I tried using a basic variance from expected measure here, but found it didn't provide as good values
    # as using the Chi-Squared test.
    
    ENGLISH_FREQ = { # Frequencies of characters in English language
        "A": 0.08497, "B": 0.01492, "C": 0.02202, "D": 0.04253, "E": 0.11162, "F": 0.02228,
        "G": 0.02015, "H": 0.06094, "I": 0.07546, "J": 0.00153, "K": 0.01292, "L": 0.04025,
        "M": 0.02406, "N": 0.06749, "O": 0.07507, "P": 0.01929, "Q": 0.00095, "R": 0.07587,
        "S": 0.06327, "T": 0.09356, "U": 0.02758, "V": 0.00978, "W": 0.02560, "X": 0.00150,
        "Y": 0.01994, "Z": 0.00077,
    }
    testStatistic = 0.0
    for c in ENGLISH_FREQ: # Iterate through all characters
        if c in message:
            freq = message.count(c) / len(message) # Get occurrence of character in shift
            letterTestStatistic = ((freq - ENGLISH_FREQ[c]) ** 2) / ENGLISH_FREQ[c] #Get test statistic
            testStatistic += letterTestStatistic #Add test statistic to total
    return testStatistic

def errorMessage(message): # Print param 'message' formatted as ERROR
    print("--- ERROR ---")
    print(f"{message}")
    print("--- ERROR ---")

def menu(): # Menu Options
    menuLoop = True
    while menuLoop: # Run until user selects to exit
        print("")
        print("--- MENU ---")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        print("--- MENU ---")
        print("")
        option = int(input("Enter option: ")) # Get input as int
        print("")
        if option == 1: # Encrypt
            decrypted = input("Enter message: ")
            key = input("Enter key: ")
            if key != "":
                print("--- START ENCRYPTION ---")
                print(f"Encrypted: {encrypt(decrypted,key)}") # Output encrypted value
                print("--- FINISH ENCRYPTION ---")
            else:
                return errorMessage("Key not specified!")
        elif option == 2: # Decrypt
            encrypted = input("Enter message: ")
            print("--- START DECRYPTION ---")
            key = solve(encrypted) # Find correct key
            print("--- KEY SOLVED ---")
            print(f"Key: {solve(encrypted)}") # Decrypt string recursively, finding correct key
            decrypted = decrypt(encrypted, key)
            print(f"Decrypted: {decrypt(encrypted,key)}") # Decrypt string recursively, finding correct key
            print("--- FINISH DECRYPTION ---")
        elif option == 3: # Exit
            print("--- GOODBYE ---")
            menuLoop = False
        else:
            return errorMessage("Invalid option!")

if __name__ == '__main__': main()