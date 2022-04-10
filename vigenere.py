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

    if mode == "interactive":
        menu()
    elif mode == "encrypt" or mode == "decrypt":
        if fileName != "":
            file = open(fileName, "r") # Open file in read mode
            decrypted = file.read() # Read file contents to string
            file.close() # Close file
            if mode == "encrypt":
                if key != "":
                    encrypt(decrypted,key,f"{fileName}.out") # Encrypt string `decrypted` with key `key` into file `[filename].out`
                else:
                    errorMessage("Key not specified!")
            elif mode == "decrypt":
                decrypt(encrypted,f"{fileName}.out")
        else:
            errorMessage("File not specified!")
    else:
        errorMessage("Invalid mode specified!")

def encrypt(decrypted, key, output=""): # Encrypt string (OPTIONAL output filename param, outputs to CLI if empty)
    print("--- START ENCRYPTION ---")

    if output == "":
        print(f"Decrypted: {decrypted}")
        print(f"Key: {key}")
    
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

    if output == "":
        print(f"Encrypted: {encrypted}")
    else:
        print(f"--- OUTPUT at '{output}' ---")
        file = open(output, "w") # Open file in write mode
        file.write(encrypted) # Write encrypted string to file contents
        file.close() # Close file

    print("--- FINISH ENCRYPTION ---")

def decrypt(encrypted, output=""): # Decrypt string (OPTIONAL output filename param, outputs to CLI if empty)
    print("--- START DECRYPTION ---")

    if output == "":
        print(f"Encrypted: {encrypted}")

    decrypted = encrypted # Do work

    if output == "":
        print(f"Decrypted: {decrypted}")
    else:
        print(f"--- OUTPUT at '{output}' ---")
        file = open(output, "w") # Open file in write mode
        file.write(decrypted) # Write decrypted string to file contents
        file.close() # Close file

    print("--- FINISH DECRYPTION ---")

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
            encrypt(decrypted,key)
        elif option == 2: # Decrypt
            encrypted = input("Enter message: ")
            decrypt(encrypted)
        elif option == 3: # Exit
            print("--- GOODBYE ---")
            menuLoop = False
        else:
            errorMessage("Invalid option!")

if __name__ == '__main__': main()