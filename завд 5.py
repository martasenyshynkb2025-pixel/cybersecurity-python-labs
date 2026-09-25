import secrets
import math

def is_probable_prime(n, k=10):
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n % p == 0:
            return n == p
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s-1):
            x = (x * x) % n
            if x == n-1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        p = secrets.randbits(bits) | (1 << (bits-1)) | 1
        if is_probable_prime(p, 12):
            return p


def generate_rsa_key(bits=2048):
    half = bits // 2
    p = generate_prime(half)
    q = generate_prime(half)
    while q == p:
        q = generate_prime(half)
    n = p * q
    phi = (p-1)*(q-1)
    e = 65537
    if math.gcd(e, phi) != 1:
        return generate_rsa_key(bits)
    d = pow(e, -1, phi)
    return {'n': n, 'e': e, 'd': d}

def info_number(name, value):
    dec = str(value)
    hex_str = hex(value)[2:].upper()
    return {
        'name': name,
        'decimal': dec,
        'decimal_digits': len(dec),
        'binary_bits': value.bit_length(),
        'hex': hex_str,
        'hex_digits': len(hex_str)
    }


print("Генеруємо RSA-ключ 2048 біт...")
key = generate_rsa_key(2048)
n, e, d = key['n'], key['e'], key['d']


n_info = info_number('n', n)
e_info = info_number('e', e)
d_info = info_number('d', d)

print("\n=== Інформація про ключ ===")
for info in (n_info, e_info, d_info):
    print(f"\n{info['name']}:")
    print("  Decimal (перші 120 символів):", info['decimal'][:120] + ("..." if info['decimal_digits']>120 else ""))
    print("  Decimal digits:", info['decimal_digits'])
    print("  Bit length:", info['binary_bits'])
    print("  Hex (перші 120 символів):", info['hex'][:120] + ("..." if info['hex_digits']>120 else ""))
    print("  Hex digits:", info['hex_digits'])


surname = "Сенишин"
surname_bytes = surname.encode('utf-8')
m = int.from_bytes(surname_bytes, byteorder='big')

if m >= n:
    raise ValueError("Повідомлення занадто велике для ключа. Використайте більший ключ або padding.")

c = pow(m, e, n)
m_decrypted = pow(c, d, n)
m2_bytes = m_decrypted.to_bytes((m_decrypted.bit_length()+7)//8, byteorder='big')
decoded = m2_bytes.decode('utf-8')

print("\n=== Шифрування / Розшифрування ===")
print("Прізвище:", surname)
print("m (integer):", m)
print("Зашифроване c (hex, початок):", hex(c)[2:80].upper() + ("..." if len(hex(c)[2:])>80 else ""))
print("Розшифроване m:", m_decrypted)
print("Розшифрований рядок:", decoded)