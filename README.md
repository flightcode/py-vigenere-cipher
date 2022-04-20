# Vigenere Cipher Decryption/Encryption
My implementation of the *Vigenere Cipher* in Python. I have documented a few challenges I found when developing the cipher, to document my reasoning for some choices. 

The decryption/encryption methods work as expected, however I could implement a better key solving method.

## Usage
```
python3 vigenere.py 
    -m (e|encrypt, d|decrypt, s|solve, i|interactive) 
    [-f <file> (required if -m not i|interactive)]
    [-k <key> (required if -m e|encrypt)]
```

## Demo
...

## Challenges
### Frequency Testing
I had issues where the frequency test biased towards shorter key lengths, which I presumed was an issue with the Chi-Squared test used. 

I moved to a basic variance from expected frequency in attempts to solve this, but found it didn't provide as good values as using the Chi-Squared test.

I then found that simply by dividing the Chi-Squared test value by the key length, the test statistic would be standardised and not bias.

### Key Solving
#### Testing All Combinations
Initially, I generated all possible keys from length 1..n (where n is the length of the the ciphertext), which proved to be inefficient at key lengths above 5.

```py
bestShifts = []
for l in range(len(ciphertext)): # Try all possible key lengths
    keys = itertools.product(string.ascii_uppercase, repeat = l) # Get all possible key combinations of length `l`
    shifts = []
    l += 1
    keyAccuracy = 0
    key = ""
    for k in keys: # Try all possible keys of length `l`
        key = "".join(k)
        decrypted = decrypt(encrypted, key) # Get decrypted string from possible key
        accuracy = freqTest(decrypted) # Get accuracy of decrypted string
        shifts.append((accuracy, key)) # Add possible shift to array
    bestShifts.append(min(shifts, key=lambda x: x[0])) # Add best key combination from this key length to `bestShifts` (Sorted by `accuracy` value of tuple)
bestKey = min(bestShifts, key=lambda x: x[0]) # Return most accurate key from `bestShifts` at all key lengths
```

#### Testing Separate Subkeys
After research, I discovered that I only needed to test each subkey from the key, testing characters once for every index in the key; as only that subkey will affect its letters in the text. By selecting only the affected characters (Every nth character starting with the lth character, where n is the index of the key, and l is the key length), and then testing the frequency, I could run tests much quicker, as a smaller dataset was being used, not repeating over the same char in the same index.

```py
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
bestKey = min(keys, key=lambda x: x[0]) # Return most accurate key from best `keys` at all key lengths
```

This reduced complexity from O(26^key_length) to O(26*key_length).

#### Dictionary Attack
I chose not to use a dictionary attack to find the key, as it was too restrictive. Using a random key would overcome this.

#### Babbage Attack & Kasiski Examination
When using the second method on larger texts (Example: Whole chapters of books), the method is still inefficient, as the potential key length to iterate through is too large.

The Kasiski Examination suggests that prior analysis of the ciphertext can reduce the potential keys by solving the key length. Meaning the solver doesn't need to iterate through all potential key lengths.

This first finds like sequences of characters (For efficiency, and based on research, tuples of length 3-5), and the spacing between these. It then finds all factors of each spacing, where the most common factors are the likely key lengths. 

By implementing this (using guidance from [Invent with Python](https://inventwithpython.com/hacking/chapter21.html)) and the previous method, the solver would be able to significantly reduce the key lengths needed to test, as well as the key combinations for each length.

**I attempted to implement this, however even when finding the repeated sequences, it still took too long to find distance between these sequences.**