
def encode():
    global numbers
    # Convert a whole message to numbers
    # Encoding
    numbers = []
    print("Encoding..")
    for i in range(len(message)):
        letter = message[i]
        n = ord(letter)
        numbers.append(n)

    print(numbers)


def decode():
    global message
    # Convert numbers to a whole message
    # Decoding
    letters = []
    print("Decoding...")
    for i in range(len(numbers)):
        n = numbers[i]
        letter = chr(n)
        letters.append(letter)

    message = "".join(letters)
    print(message)


def decrypt(offset):
    print("Decrypting...")
    for i in range(len(numbers)):
        if not numbers[i] == 32:
            numbers[i] -= offset
            if numbers[i] < 97:
                numbers[i] += 26


def encrypt(offset):
    print("Encrypting...")
    for i in range(len(numbers)):
        if not numbers[i] == 32:
            numbers[i] += offset
            if numbers[i] > 122:
                numbers[i] -= 26


print("Enter message to be encoded:")
message = "hello world"

numbers = [
    108, 117, 106, 118, 107, 108, 107, 32, 112, 117, 32, 104, 117, 32, 104, 117, 106, 112, 108, 117,
    97, 32, 121, 118, 116, 104, 117, 32, 106, 112, 119, 111, 108, 121,
]

encode()
encrypt(10)
decode()

encode()
decrypt(10)
decode()