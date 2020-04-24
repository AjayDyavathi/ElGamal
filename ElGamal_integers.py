import random


def generate_prime_factors(n):
    i = 2
    prime_factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            if i not in prime_factors:
                prime_factors.append(i)
    if n > 1:
        prime_factors.append(n)
    return prime_factors


def find_primitive_root(p):
    '''returns a primitive_root-generator for given prime number p'''
    order = p - 1   # phi(p)

    if p == 2:
        return 1

    # the prime factors of "order" are 2 and (p-1)/2
    # consider a random number g from 2 to p-1
    # check if g**(order/x) mod p == 1 where x is iterated through all prime factors
    # if true then, g is not a generator, choose another g until it gets false

    prime_factors = generate_prime_factors(order)

    while True:
        g = random.randint(2, order)

        flag = False
        for factor in prime_factors:
            # pow -> pow(base, exponent, modulo)
            if pow(g, order // factor, p) == 1:
                flag = True
                break
        if flag:
            continue
        return g


def generate_keys(prime):
    '''generates public_key, private_key pair'''

    p = prime
    g = find_primitive_root(p)
    x = random.randint(1, (p - 1) // 2)
    h = pow(g, x, p)

    private_key = x
    public_key = h
    return (public_key, private_key), g


def encrypt(public_key, prime, g):
    '''This encryption is done other side of communication
    A secret message is encrypted with given parameters
    then,  encrypted_msg and ephemeral_key are sent back'''

    # secret_message = 21
    print("Now assume you're on other side...")
    secret_message = int(input('Enter any number to encrypt: '))
    y = random.randint(1, (prime - 1) // 2)
    ephemeral_key = pow(g, y, prime)
    masking_key = pow(public_key, y, prime)

    return (secret_message * masking_key) % prime, ephemeral_key


# This is done on the owner side
# prime_number = 1237
prime_number = int(input('Enter any prime number: '))
print('Generating keys...')
keys, generator = generate_keys(prime_number)
public_key, private_key = keys
print(f'public key: {public_key}, private_key: {private_key}')
print('Transmitting public_key, prime_number, generator publicly.....\n')

# sending our public_key, prime_number, generator to others for encryption

cipher, ephemeral_key = encrypt(public_key, prime_number, generator)
print()
print('ciphertext recieved..')
# what we recieve is a cipher and temporary session key called "ephermeral_key"
print('ciphertext:', cipher, 'ephemeral_key:', ephemeral_key)
print()

# decrypt the encrypted message on our side
# computing the masking key from ephermeral_key
print('Computing Masking key...')
masking_key = pow(ephemeral_key, prime_number - 1 - keys[1])
decipher = (cipher * masking_key) % prime_number
print('decrypted:', decipher)
