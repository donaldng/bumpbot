from cryptography.fernet import Fernet as f
import os.path

# documentation - https://cryptography.io/en/latest/fernet/

def encrypt(string):
    return f(privkey()).encrypt(string.encode('utf-8')).decode('utf-8')

def decrypt(token):
    try:
        result = f(privkey()).decrypt(token.encode("utf-8")).decode('utf-8')
    except:
        result = None        
        print("Invalid token or string cannot be decrypted through private key!")

    return result

def privkey():
    path = '.privatekey'

    if not os.path.isfile(path):
        pk = f.generate_key().decode('utf-8')
        
        file = open(path,"w") 
        file.write(pk)
        file.close()
    else:
        with open(path, 'rb') as secret:
            pk = secret.read()
    
    return pk