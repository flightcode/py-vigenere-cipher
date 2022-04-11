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
                decrypted = solve(text) # Decrypt string recursively, finding correct key
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
    bestShifts = []
    for l in range(1,len(encrypted)): # Try all possible key lengths
        print(f"Trying key length {l}...")
        keys = itertools.product(string.ascii_uppercase, repeat = l) # Get all possible key combinations of length `l`
        shifts = []
        for k in keys: # Try all possible keys of length `l`
            key = "".join(k)
            decrypted = decrypt(encrypted, key) # Get decrypted string from possible key
            accuracy = freqTest(decrypted) # Get accuracy of decrypted string
            shifts.append((accuracy, key)) # Add possible shift to array
        bestShifts.append(min(shifts, key=lambda x: x[0])) # Add best key combination from this key length to `bestShifts` (Sorted by `accuracy` value of tuple)
        print(f"Best key at length {l} = {min(shifts, key=lambda x: x[0])}")
    bestKey = min(bestShifts, key=lambda x: x[0]) # Return most accurate key from `bestShifts` at all key lengths
    print(f"Best key overall = {bestKey[1]}")
    return decrypt(encrypted, bestKey[1]) # Return decryption using `bestKey`

def freqTest(message): # Test frequency of string against English language alphabet frequencies (0 is most accurate)
    FREQUENCIES = { #Frequencies of characters in English language
        "a": 0.08497, "b": 0.01492, "c": 0.02202, "d": 0.04253, "e": 0.11162, "f": 0.02228,
        "g": 0.02015, "h": 0.06094, "i": 0.07546, "j": 0.00153, "k": 0.01292, "l": 0.04025,
        "m": 0.02406, "n": 0.06749, "o": 0.07507, "p": 0.01929, "q": 0.00095, "r": 0.07587,
        "s": 0.06327, "t": 0.09356, "u": 0.02758, "v": 0.00978, "w": 0.02560, "x": 0.00150,
        "y": 0.01994, "z": 0.00077,
    }
    testStatistic = 0.0
    for c in message: #Iterate through all characters in shift
        if c in FREQUENCIES:
            occ = message.count(c) #Get occurrence of characters in shift
            occ_expected = FREQUENCIES[c] * occ #Get expected occurrence from frequencies
            letterTestStatistic = ((occ - occ_expected) ** 2) / occ_expected #Get test statistic
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
            print(f"Decrypted: {solve(encrypted)}") # Decrypt string recursively, finding correct key
            print("--- FINISH DECRYPTION ---")
        elif option == 3: # Exit
            print("--- GOODBYE ---")
            menuLoop = False
        else:
            return errorMessage("Invalid option!")

if __name__ == '__main__': main()