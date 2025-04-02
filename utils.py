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




def generateCert():
    country = input("Enter your country (2 Letter format): ")
    state = input("Enter your state: ")
    city = input("Enter your city: ")
    organizationname = input("Enter the name of your organization: ")
    commonname = input("Enter your common/program name: ")


    pw = getpass("Enter your password: ")
    with open("Vault/rsa.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=pw.encode('utf-8')
        )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, city),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organizationname),
        x509.NameAttribute(NameOID.COMMON_NAME, commonname),
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
    ).sign(private_key, hashes.SHA256())

    with open("Vault/certificate.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


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
    #CONVERTS ENCRYPTED DATA TO STRING FORMAT FOR PRINTING
    #return base64.b64encode(ciphertext).decode('utf-8')


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
