"""Тестовий файл для ознайомлення з правилами форматування і оформлення коду
згідно Python Enhancement Proposals PEP 8 – Style Guide for Python Code."""

import string
import time

SHIFT = 3
PI = 3.14

def print_time(show_time):
    """Функція друкує поточний час, якщо передано True."""
    if show_time:
        print(time.ctime())


def main():
    """gggggggggggggg"""
    choice_mode = input("Would you like to encode or decode? ")
    word = input("Please enter text: ")
    letters = string.ascii_letters + string.punctuation + string.digits
    encoded = ""

    if choice_mode == "encode":
        for letter in word:
            if letter == " ":
                encoded += " "
            else:
                index = letters.index(letter)
                new_index = (index + SHIFT) % len(letters)
                encoded += letters[new_index]

    elif choice_mode == "decode":
        for letter in word:
            if letter == " ":
                encoded += " "
            else:
                index = letters.index(letter)
                new_index = (index - SHIFT) % len(letters)
                encoded += letters[new_index]

    else:
        print("Invalid mode selected. Please choose 'encode' or 'decode'.")
        return

    print("Result:", encoded)
    print_time(True)

if __name__ == '__name__':
    main()
