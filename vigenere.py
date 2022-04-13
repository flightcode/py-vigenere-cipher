#!/usr/bin/env python3

# Vigenere cipher encoder/decoder/solver.
# github.com/flightcode
# 2022
# USAGE: 
#   ./vigenere.py 
#       -m (e|encrypt, d|decrypt, s|solve, i|interactive) 
#       [-f <file> (required if -m not i|interactive)]
#       [-k <key> (required if -m e|encrypt)]

import sys # For CLI rguments
import getopt # Parses CLI arguments
import itertools # Code-efficient iterators
import string

def main(): # Welcome message and run menu
    print("--- VIGENERE CIPHER ----")
    print("--- FLIGHTCODE 2022 ----")

    mode = "" # Interactive for testing or if user wants a menu
    fileName = "" # File to parse
    key = "" # Required for encode.

    try: # Attempt to parse arguments (Strip first argument (Command))
        opts, args = getopt.getopt(sys.argv[1:], "hm:f:k:", ["help","mode=","file=","key="])
    except:
        errorMessage("Unable to parse arguments!")
        print('Usage: ./vigenere.py -m <mode> -f <file> -k <key>')
        print('Modes: e|encrypt')
        print('       d|decrypt')
        print('       s|solve')
        print('       i|interactive')
        exit()

    for opt, arg in opts: # Assign from arguments 
        if opt in ["-h","--help"]:
            print('Usage: ./vigenere.py -m <mode> -f <file> -k <key>')
            print('Modes: e|encrypt')
            print('       d|decrypt')
            print('       s|solve')
            print('       i|interactive')
            exit()
        elif opt in ["-f","--file"]:
            fileName = arg
        elif opt in ["-m","--mode"]:
            mode = arg
        elif opt in ["-k","--key"]:
            key = arg

    if mode == "interactive" or mode == "i":
        menu()
    elif mode == "encrypt" or mode == "e" or mode == "decrypt" or mode == "d" or mode == "solve" or mode == "s":
        if fileName != "":
            with open(fileName, "r") as file: # Open file in read mode
                text = file.read() # Read file contents to string
            if mode == "encrypt" or mode == "e":
                if key != "":
                    print("--- START ENCRYPTION ---")
                    ciphertext = encrypt(text,key) # Encrypt string `decrypted` with key `key`
                    with open(f"{fileName}.out", "w") as file: # Open file in write mode
                        file.write(ciphertext) # Write encrypted string to file contents
                    print(f"--- OUTPUT to '{fileName}.out' ---")
                    print("--- FINISH ENCRYPTION ---")
                else:
                    return errorMessage("Key not specified!")
            elif mode == "decrypt" or mode == "d":
                if key != "":
                    print("--- START DECRYPTION ---")
                    plaintext = decrypt(text, key)
                    with open(f"{fileName}.out", "w") as file: # Open file in write mode
                        file.write(plaintext) # Write decrypted string to file contents
                    print("--- FINISH DECRYPTION ---")
                else:
                    return errorMessage("Key not specified!")
            elif mode == "solve" or mode == "s":
                print("--- START DECRYPTION ---")
                key = solve(text) # Find correct key
                print("--- KEY SOLVED ---")
                plaintext = decrypt(text, key)
                with open(f"{fileName}.out", "w") as file: # Open file in write mode
                    file.write(plaintext) # Write decrypted string to file contents
                print("--- FINISH DECRYPTION ---")
        else:
            return errorMessage("File not specified!")
    else:
        return errorMessage("Invalid mode specified!")

def encrypt(plaintext, key): # Encrypt string with given key    
    # Encrypts using iterated-key method, where for each character in string, 
    # character is encrypted by nth character in string (modulo key length. 
    # This simulates a key of same length as string, but is more memory efficient)

    key = key.upper()
    lowerStart = ord('a') # Start shift for 'a' in lowercase
    upperStart = ord('A') # Start shift for 'A' in uppercase
    ciphertext = ""

    i = 0
    for c in plaintext:
        if c.isalpha():
            if c.isupper(): # Uppercase shift
                start = upperStart
            else: # Lowercase shift
                start = lowerStart

            cPos = ord(c) - start # Get position of char
            shift = ord(key[i % len(key)]) - upperStart # Get shift amount based on keyPos (Key is in uppercase)
            cNewPos = (cPos + shift) % 26 # Get position of shifted char
            
            ciphertext += chr(cNewPos + start) # Add character to encrypted string
            i += 1
        else: # If not alphanumeric
            ciphertext += c
    return ciphertext

def decrypt(ciphertext, key): # Decrypt string with given key
    # Decrypts using iterated-key method, where for each character in string, 
    # character is decrypted by nth character in string (modulo key length. 
    # This simulates a key of same length as string, but is more memory efficient)
    
    key = key.upper()
    lowerStart = ord('a') # Start shift for 'a' in lowercase
    upperStart = ord('A') # Start shift for 'A' in uppercase
    plaintext = ""

    i = 0
    for c in ciphertext:
        if c.isalpha():
            if c.isupper(): # Uppercase shift
                start = upperStart
            else: # Lowercase shift
                start = lowerStart

            cPos = ord(c) - start # Get position of char
            shift = ord(key[i % len(key)]) - upperStart # Get reverseshift amount based on keyPos (Key is in uppercase)
            cNewPos = (cPos - shift) % 26 # Get position of shifted char
            
            plaintext += chr(cNewPos + start) # Add character to decrypted string
            i += 1
        else: # If not alphanumeric
            plaintext += c
    return plaintext

def solve(ciphertext): # Get key of encrypted string
    ciphertextTrimmed = [c for c in ciphertext.upper() if c in string.ascii_uppercase]
    keys = []
    for l in range(len(ciphertext)): # Try all possible key lengths
        l += 1
        keyAccuracy = 0
        key = ""
        for i in range(l): # Iterate through nth letter of key length
            affectedLetters = "".join(itertools.islice(ciphertextTrimmed, i, None, l)) # Get every nth letter from `encrypted`
            shifts = []
            for c in string.ascii_uppercase: # Try all possible characters for nth letter
                plaintext = decrypt(affectedLetters, c) # Get decrypted string from possible key
                accuracy = freqTest(plaintext) # Get accuracy of decrypted string
                shifts.append((accuracy, c)) # Add possible shift to array
            bestChar = min(shifts, key=lambda x: x[0])
            keyAccuracy += (bestChar[0] / l) # Add char accuracy to key accuracy, divide by key_length avoids biasing for smaller keys
            key += bestChar[1]
        keys.append((keyAccuracy,key))
        # print(f"Best key at length {l} = {(keyAccuracy,key)}") # DEBUGGING
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
        print("3. Solve (Decrypt without key)")
        print("4. Exit")
        print("--- MENU ---")
        print("")
        option = int(input("Enter option: ")) # Get input as int
        print("")
        if option == 1: # Encrypt
            plaintext = input("Enter message: ")
            key = input("Enter key: ")
            if key != "":
                print("--- START ENCRYPTION ---")
                print(f"Encrypted: {encrypt(plaintext,key)}") # Output encrypted value
                print("--- FINISH ENCRYPTION ---")
            else:
                return errorMessage("Key not specified!")
        elif option == 2: # Decrypt
            ciphertext = input("Enter message: ")
            key = input("Enter key: ")
            print("--- START DECRYPTION ---")
            print(f"Decrypted: {decrypt(ciphertext,key)}") # Output decrypted value
            print("--- FINISH DECRYPTION ---")
        elif option == 3: # Solve (Decrypt without Key)
            ciphertext = input("Enter message: ")
            print("--- START DECRYPTION ---")
            key = solve(ciphertext) # Find correct key
            print("--- KEY SOLVED ---")
            print(f"Key: {key}") # Decrypt string recursively, finding correct key
            print(f"Decrypted: {decrypt(ciphertext,key)}") # Decrypt string with correct key
            print("--- FINISH DECRYPTION ---")
        elif option == 4: # Exit
            print("--- GOODBYE ---")
            menuLoop = False
        else:
            return errorMessage("Invalid option!")

if __name__ == '__main__': main()