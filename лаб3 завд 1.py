ukr_letters = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
key = 23

encrypted_message = 'Пмцфкйіц рмп'

decrypted_message = ''

for char in encrypted_message:
    if char.lower() in ukr_letters:
        index = ukr_letters.index(char.lower())
        new_index = (index - key) % len(ukr_letters)
        decrypted_char = ukr_letters[new_index]

        if char.isupper():
            decrypted_char = decrypted_char.upper()

        decrypted_message += decrypted_char
    else:
        decrypted_message += char

print("TASK 1: Decrypt message")
print(f"KEY: {key}")
print(f"\nEncrypted Message:\n{encrypted_message}")
print(f"\nDecrypted message:\n{decrypted_message}")