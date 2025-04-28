import random
from js import document

list_of_primes = [
    1085677223, 1088946217, 1123919243, 1346745143, 1480531453, 1745585321, 2180663851,
    2232791993, 2317816603, 2538185753, 2641218641, 3068653447, 3105901181, 3137544353,
    3212147311, 3341150531, 3382876577, 3486412693, 3523241287, 3704501641, 3802613041,
    3832739359, 4003276579, 4583406749, 4725356011, 4729771561, 4968782677, 5180490191,
    5490161461, 5659552853, 5713505377, 6114973273, 6168826973, 6583975217, 6607106447,
    6707124367, 6739472837, 6767531369, 6919620049, 7404006971, 7439432293, 7881164747,
    8070104291, 8479331771, 8811132679, 9262348517, 9609798127, 9686516813, 9700856941,
    9948117007
]

e_values = [12301, 87121, 19793, 45989, 30113, 52361, 96731, 63149, 70313, 81223]

#all RSA encryption and decryption functions 
#I would put this in a seperate file normally but py-script 
# was throwing an error and I couldn't figure it out
def modular_inverse(x, y):
    if gcd(x, y) > 1:
        ValueError("GCD > 1")
    for i in range(1, y):
        if (((x % y) * (i % y)) % y == 1):
            return i
    raise ValueError("mod inverse does not exist")

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def is_prime(n):
    # check the most common divisors 
    if n <= 1:
        return False
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # start at 5 cause if n % 4 == 0 then n % 2 == 0
    for i in range(5,int(n/2)):
        if n % i == 0:
            return False
    return True     

def RSA_preperation(p, q, e):
    if not is_prime(q) or not is_prime(p):
        raise ValueError("p or q is not prime") 

    phi_n = (p-1) * (q-1)
    if gcd(e, phi_n) != 1:
        raise ValueError("e must be Coprime with Phi_n")
    d = modular_inverse(e, phi_n)
    return d

def RSA_decrypt(c, p, q, e):
    d = RSA_preperation(p, q, e)
    N = p * q
    return pow(c, d, N)

# just for testing 
def RSA_encrypt(m, e, N):
    return pow(m, e, N) 
    

# Save p, q, e, N globally so we can reuse

def setup_keys():
    random.shuffle(list_of_primes)
    p = list_of_primes.pop()
    q = list_of_primes.pop()
    while p == q:
        q = list_of_primes.pop()

    N = p * q
    phi_N = (p-1)*(q-1)

    e = 65537
    if e >= phi_N or gcd(e, phi_N) != 1:
        random.shuffle(e_values)
        while e >= phi_N or gcd(e, phi_N) != 1:
            e = e_values.pop()

    return p, q, e, N            


