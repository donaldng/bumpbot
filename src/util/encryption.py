from cryptography.fernet import Fernet as f
import os.path

# documentation - https://cryptography.io/en/latest/fernet/

class CryptoFernet:
    def __init__(self):
        path = '.privatekey'

        if not os.path.isfile(path):
            self.pk = f.generate_key().decode('utf-8')
            
            file = open(path,"w") 
            file.write(self.pk)
            file.close()
        else:
            with open(path, 'rb') as secret:
                self.pk = secret.read()

    def encrypt(self, string):
        return f(self.pk).encrypt(string.encode('utf-8')).decode('utf-8')

    def decrypt(self, token):
        try:
            result = f(self.pk).decrypt(token.encode("utf-8")).decode('utf-8')
        except:
            result = None        
            log("Invalid token or string cannot be decrypted through private key!")

        return result
