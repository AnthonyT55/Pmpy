from getpass import getpass
import hashlib, secrets, os, base64, datetime, platform
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding



def generate_salt(length=16):
    salt = secrets.token_bytes(length)
    return salt

def getsecretkeyfromstring(data):
    """RETURNS A HASHED VERSION OF YOUR SECRET KEY DERIVES IT FROM THE STRING INPUT OF YOUR SECRET KEY"""
    h = hashlib.sha256()

    h.update(data.encode('utf-8'))

    secretkey = h.hexdigest()

    return secretkey


def generatekeys():
    password = getpass("Enter your password: ")

    privkey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    encrypted_pem_private_key = privkey.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8')))

    pem_public_key = privkey.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    privkeyfile = "Vault/rsa.pem"
    os.makedirs(os.path.dirname(privkeyfile), exist_ok=True)
    with open(privkeyfile, "w") as f:
        f.write(encrypted_pem_private_key.decode())

    pubkeyfile = "Vault/rsa.pub"
    os.makedirs(os.path.dirname(pubkeyfile), exist_ok=True)
    with open(pubkeyfile, "w") as f:
        f.write(pem_public_key.decode())

    print("RSA key pair encoded and saved to filesystem (Check for a folder named 'Vaults')")

def clearScreen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')





def encryptData(data):
    with open("Vault/rsa.pub", "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
        )

    ciphertext = public_key.encrypt(
        data.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext
    


def decryptData(data, decryptionpw):
    try:
        with open("Vault/rsa.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=decryptionpw.encode('utf-8'),
            )
        
        
        
    except:
        print("INCORRECT PASSWORD")

    decryptedData = private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    return decryptedData






#print(encryptData("potato"))
#print(decryptData(encryptData("potato")))
#generateCert(country, state, city, organizationname, commonname)


