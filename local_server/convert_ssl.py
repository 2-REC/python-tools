from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization

pfx_path = "cert.pfx"
pfx_password = b"password"  # use b"" for no password

with open(pfx_path, "rb") as f:
    pfx_data = f.read()

# load PFX data
private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
    pfx_data, 
    pfx_password
)

# save private key
with open("key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# save certificate
with open("cert.pem", "wb") as f:
    f.write(certificate.public_bytes(serialization.Encoding.PEM))
    if additional_certs:
        for ca in additional_certs:
            f.write(ca.public_bytes(serialization.Encoding.PEM))

print("Successfully created key.pem and cert.pem")
