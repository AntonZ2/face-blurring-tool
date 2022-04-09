# performs logical AND operation on items in lists (A AND B)
def list_and(i, j): return [A & B for A, B in zip(i, j)]


# performs logical NOT operation on items in lists
def list_not(i): return [~x for x in i]


# performs logical XOR operation on items in lists
def list_xor(i, j): return [A ^ B for A, B in zip(i, j)]


# performs logical XOR operation on 3 consecutive items in list (A XOR (B XOR C))
def list_double_xor(i, j, k): return [A ^ (B ^ C) for A, B, C, in zip(i, j, k)]


# performs rotation rightwards of items in a list by n places (x = [1,2,3,4,5], list_rotate(x,2) = [5,4,1,2,3])
def list_rotate(x, n): return x[-n:] + x[:-n]


# shifts items rightwards in the list by n places (x = [1,2,3,4,5], list_shift(x,2) = [0,0,5,4,3]
def list_shift(x, n): return n * [0] + x[:-n]


# performs binary addition of items of two lists getting rid of carry over bits beyond set length
def list_add(i, j):
    length = len(i)
    added = list(range(length))
    c = 0
    for x in range(length-1, -1, -1):
        added[x] = i[x] ^ (j[x] ^ c)
        c = max([i[x], j[x]], key=[i[x], j[x], c].count)
    return added


class Hashing:
    def __init__(self):
        # hash values which are the first 32 bits of the fractional parts of the square roots of the first 8 primes
        self.hex = ['0x6a09e667', '0xbb67ae85', '0x3c6ef372', '0xa54ff53a',
                    '0x510e527f', '0x9b05688c', '0x1f83d9ab', '0x5be0cd19']

        # constants which are the first 32 bits of the fractional parts of the cube roots of the first 64 primes
        self.constants = ['0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5', '0x3956c25b', '0x59f111f1',
                          '0x923f82a4', '0xab1c5ed5', '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3',
                          '0x72be5d74', '0x80deb1fe', '0x9bdc06a7', '0xc19bf174', '0xe49b69c1', '0xefbe4786',
                          '0x0fc19dc6', '0x240ca1cc', '0x2de92c6f', '0x4a7484aa', '0x5cb0a9dc', '0x76f988da',
                          '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7', '0xc6e00bf3', '0xd5a79147',
                          '0x06ca6351', '0x14292967', '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc', '0x53380d13',
                          '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85', '0xa2bfe8a1', '0xa81a664b',
                          '0xc24b8b70', '0xc76c51a3', '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070',
                          '0x19a4c116', '0x1e376c08', '0x2748774c', '0x34b0bcb5', '0x391c0cb3', '0x4ed8aa4a',
                          '0x5b9cca4f', '0x682e6ff3', '0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208',
                          '0x90befffa', '0xa4506ceb', '0xbef9a3f7', '0xc67178f2']

        self.encryption_key = 27

    def string_to_binary(self, text):
        # converts the text to integer representation in unicode
        utf_codes = [ord(char) for char in text]
        # converts unicode integers to binary bytes
        binarybytes = []
        for char in utf_codes:
            binarybytes.append(bin(char)[2:].zfill(8))
        # splits bytes into bits and converts to integers from strings
        bits = []
        for i in binarybytes:
            for bit in i:
                bits.append(int(bit))
        return bits

    def bin_to_hex(self, value):
        # stores binary list as a string to convert to hexadecimal
        string = ''
        for i in value:
            string += str(i)
        x = hex(int('0b' + string, 2))
        # stores the hex value without python datatype identifier
        hexes = x[2:]
        return hexes

    def chunker(self, bits, length=8):
        # splits up the bits into byte chunks
        chunks = []
        for i in range(0, len(bits), length):
            chunks.append(bits[i:i+length])
        return chunks

    def pad_zeroes(self, bits, length=8, endian='little'):
        # append zeroes or prepends zeroes until the desired length of bits is reached
        x = len(bits)
        # if endian is little then appends zeroes after the bits
        if endian == 'little':
            for i in range(x, length):
                bits.append(0)
        # if endian is big then inserts zeroes before the bits
        else:
            for j in range(length - x):
                bits.insert(0, 0)
        return bits

    def pad_message(self, text):
        # translate message into bits
        bits = self.string_to_binary(text)
        length = len(bits)
        # get length in bits  of message in 64 bit blocks
        text_len = [int(b) for b in bin(length)[2:].zfill(64)]
        # if length smaller than 448 handle block individually otherwise
        # pads with zeroes till length is 64 characters short of a multiple of 512
        if length < 448:
            # append single 1
            bits.append(1)
            # pads the zeroes
            bits = self.pad_zeroes(bits, 448, 'little')
            bits = bits + text_len
            return [bits]
        elif 448 <= length <= 512:
            # append single 1
            bits.append(1)
            # pads the zeroes

            bits = self.pad_zeroes(bits, 1024, 'little')
            # last 64 bits represent original message length
            bits[-64:] = text_len
            return self.chunker(bits, 512)
        else:
            bits.append(1)
            # loop until multiple of 512 if message is longer than 448 bits
            while len(bits) % 512 != 0:
                bits.append(0)
            # last 64 bits represent original message length
            bits[-64:] = text_len
        return self.chunker(bits, 512)

    def words_to_32bit(self, values):
        # converts from hex to binary without python datatype code
        binaries = [bin(int(v, 16))[2:] for v in values]
        # creates 2D list containing 32 bit words in binary
        words = []
        for binary in binaries:
            word = []
            for b in binary:
                word.append(int(b))
            # pad zeroes before word to make 32 bit length
            words.append(self.pad_zeroes(word, 32, 'big'))
        return words

    def sha256(self, text):
        # converts hard coded constants into 32bit
        k = self.words_to_32bit(self.constants)
        # converts hard coded hash values into 32bit
        h0, h1, h2, h3, h4, h5, h6, h7 = self.words_to_32bit(self.hex)
        # splits up input text into chunks
        chunks = self.pad_message(text)
        for chunk in chunks:
            words = self.chunker(chunk, 32)
            for x in range(48):
                # add 48 empty words to list to make 64 total words
                words.append(32*[0])
            for i in range(16, 64):
                # performs SHA256 hash function on list of words
                sigma0 = list_double_xor(list_rotate(words[i - 15], 7),
                                         list_rotate(words[i - 15], 18), list_shift(words[i - 15], 3))
                sigma1 = list_double_xor(list_rotate(words[i - 2], 17), list_rotate(words[i - 2], 19),
                                         list_shift(words[i - 2], 10))
                words[i] = list_add(list_add(list_add(words[i - 16], sigma0), words[i - 7]), sigma1)
            a = h0
            b = h1
            c = h2
            d = h3
            e = h4
            f = h5
            g = h6
            h = h7
            for j in range(64):
                sigma1 = list_double_xor(list_rotate(e, 6), list_rotate(e, 11), list_rotate(e, 25))
                ch = list_xor(list_and(e, f), list_and(list_not(e), g))
                temp1 = list_add(list_add(list_add(list_add(h, sigma1), ch), k[j]), words[j])
                sigma0 = list_double_xor(list_rotate(a, 2), list_rotate(a, 13), list_rotate(a, 22))
                m = list_double_xor(list_and(a, b), list_and(a, c), list_and(b, c))
                temp2 = list_add(sigma0, m)
                h = g
                g = f
                f = e
                e = list_add(d, temp1)
                d = c
                c = b
                b = a
                a = list_add(temp1, temp2)
            h0 = list_add(h0, a)
            h1 = list_add(h1, b)
            h2 = list_add(h2, c)
            h3 = list_add(h3, d)
            h4 = list_add(h4, e)
            h5 = list_add(h5, f)
            h6 = list_add(h6, g)
            h7 = list_add(h7, h)
        # creates an output variable to stored hashed value of inputted text
        output = ''
        # inserts the 8 binary text values created
        for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
            # final form reached by converting from binary to hexadecimal
            output += self.bin_to_hex(val)
        return output

    '''def image_encryption(self, image):
        image = bytearray(image)
        for index, values in enumerate(image):
            image[index] = values ^ self.encryption_key
        return image'''

