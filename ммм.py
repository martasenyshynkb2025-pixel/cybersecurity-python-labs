import string, os, math, time

def PrintTime(x):
    if x == True:
        print(time.ctime())
    return

def main():
    shift = 3  # зсув для шифрування

    Choice_mode = input("Would you like to encode or decode: ")
    word = input("Please enter text: ")

    LETTERS = string.ascii_letters + string.punctuation + string.digits
    encoded = ""

    if Choice_mode == "encode":
        for letter in word:
            if letter == " ":
                encoded += " "
            else:
                x = LETTERS.index(letter) + shift
                encoded += LETTERS[x % len(LETTERS)]
        print("Encoded text:", encoded)

    elif Choice_mode == "decode":
        for letter in word:
            if letter == " ":
                encoded += " "
            else:
                x = LETTERS.index(letter) - shift
                encoded += LETTERS[x % len(LETTERS)]
        print("Decoded text:", encoded)

    print("Original text:", word)

if __name__ == "__main__":
    main()