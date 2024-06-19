import os

from OpenSSL import crypto, SSL
from os.path import exists, join


def create_self_signed_cert(CN: str):
    try:
        os.mkdir('./certificates')
    except:
        print("Just warning: Path already exist or user haven't write permission ('certificates' directory creation)")

    CERT_FILE = f"certificates/{CN}.crt"
    KEY_FILE = f"certificates/{CN}.key"

    if not exists(CERT_FILE) or not exists(KEY_FILE):
        # Create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)

        # Create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "California"
        cert.get_subject().L = "San Francisco"
        cert.get_subject().O = "Electronic Frontier Foundation, Inc."
        cert.get_subject().CN = CN
        cert.set_serial_number(1)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(31536000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')

        # Write the certificate and key to files
        with open(CERT_FILE, "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())
        with open(KEY_FILE, "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode())