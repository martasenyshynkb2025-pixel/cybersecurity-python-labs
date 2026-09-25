
surname = "Сенишин"


key = "mysecretkey"


surname_bytes = surname.encode('utf-8')
key_bytes = key.encode('utf-8')


cipher_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(surname_bytes)])


decrypted_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(cipher_bytes)])
decrypted_surname = decrypted_bytes.decode('utf-8')


print("Оригінал:", surname)
print("Байти оригіналу (hex):", surname_bytes.hex().upper())
print("Зашифрований текст (hex):", cipher_bytes.hex().upper())
print("Розшифрований текст:", decrypted_surname)