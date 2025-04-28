import random
from js import document
from pyodide.ffi import create_proxy

list_of_primes = [
    101, 113, 131, 151, 179,
    193, 211, 227, 263, 281,
    307, 359, 389, 419, 457,
    509, 557, 613, 673, 743
]

e_values = [11, 17, 23, 31, 41, 53, 61, 73, 83, 97]

def modular_inverse(x, y):
    if gcd(x, y) > 1:
        raise ValueError("GCD > 1")
    for i in range(1, y):
        if (((x % y) * (i % y)) % y == 1):
            return i
    raise ValueError("mod inverse does not exist")

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def is_prime(n):
    if n <= 1:
        return False
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n/2)):
        if n % i == 0:
            return False
    return True     

def RSA_preparation(p, q, e):
    if not is_prime(q) or not is_prime(p):
        raise ValueError("p or q is not prime") 
    phi_n = (p-1) * (q-1)
    if gcd(e, phi_n) != 1:
        raise ValueError("e must be Coprime with Phi_n")
    d = modular_inverse(e, phi_n)
    return d

def RSA_encrypt(m, e, N):
    return pow(m, e, N)

def RSA_decrypt(c, p, q, e):
    d = RSA_preparation(p, q, e)
    N = p * q
    return pow(c, d, N)

# Generate p, q, e, N
def setup_keys():
    p, q = random.sample(list_of_primes, 2)
    N = p * q
    phi_N = (p-1)*(q-1)
    e = random.choice(e_values)
    while gcd(e, phi_N) != 1:
        e = random.choice(e_values)
    return p, q, e, N

# MAIN FUNCTION to bind to button
def run_rsa(event=None):
    p, q, e, N = setup_keys()
    d = modular_inverse(e, (p-1)*(q-1))
    phi_n = (q-1) * (p-1)
    input_box = document.getElementById("RSA_in")
    generated = document.getElementById("generated")
    ascii_display = document.getElementById("ascii_display")
    encoded = document.getElementById("encoded")
    decoded = document.getElementById("decoded")

    message = input_box.value
    asc_ii = [ord(c) for c in message]
    cipher = [RSA_encrypt(m, e, N) for m in asc_ii]
    plain = [chr(RSA_decrypt(c, p, q, e)) for c in cipher]

    # Output results
    generated.innerText = (
        f"Public Key (e, N): ({e}, {N})\n"
        f"Private Key Formula: d ≡ e⁻¹ mod φ(N)\n"
        f"  d = {d}"
    )
    ascii_display.innerText = f"ASCII codes: {asc_ii}"
    encoded.innerText = (f"Encoded (ciphertext numbers): {cipher}")
    decoded.innerText = f"Decoded (plaintext): {''.join(plain)}"

# Bind to button click
button = document.getElementById("start_rsa")
run_rsa_proxy = create_proxy(run_rsa)
button.addEventListener("click", run_rsa_proxy)
