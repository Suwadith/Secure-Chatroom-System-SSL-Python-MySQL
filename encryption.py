import cryptocode


def encrypt_password(password):
    encrypted_password = cryptocode.encrypt(password, "secret_key")
    return encrypted_password


def decrypt_password(encrypted_password, password):
    decrypted_password = cryptocode.decrypt(encrypted_password, "secret_key")
    print(decrypted_password)
    if decrypted_password == password:
        return True
    else:
        return False


def encrypt_message(message):
    encrypted_message = cryptocode.encrypt(message, "secret_message")
    return encrypted_message


# print(encrypt_password("killme"))
#
# print(decrypt_password("r43cKlA7*RRmYmaI2uN0TmNlwH+3htw==*Jt03qXXqYj5vPQHbENTOzw==*yaXFD4gZllcq3RE5SJ32KA==", "killme"))