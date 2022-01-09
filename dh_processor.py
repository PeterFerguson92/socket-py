def generate_key(public_key_1,private_key, public_key_2):
    return int(pow(public_key_1, private_key, public_key_2))

def encrypt_message(message, key):
    print(message)
    encrypted_message = ""
    for c in message:
        encrypted_message += chr(ord(c)+key)
    return encrypted_message    

def decrypt_message(encrypted_message, key):
    decrypted_message = ""
    for c in encrypted_message:
        decrypted_message += chr(ord(c)-key)
    return decrypted_message