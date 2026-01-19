# Python Local Server

Lightweight local web server for testing purpose.

Some steps specific to Windows (SSL certificate).

> **NOTE:** Python installation might not be in PATH.
> It is generally installed in "C:\Users\ADMIN\AppData\Local\Programs\Python\Python311".

---
## Setup

### Virtual Environment

Steps to setup the environment:
* Upgrade pip
    ```
    python.exe -m pip install --upgrade pip
    ```
* Install virtualenv
    ```
    python -m pip install --user virtualenv
    ```
* Create virtual environment:
    ```
    python -m vitualenv <ENV_NAME>
    ```
    E.g.:
    ```
    python -m vitualenv python_http_server
    ```
* Start virtual environment:
    ```
    .\<ENV_NAME>\Scripts\activate
    ```

### HTTPS - SSL Certificate

To support serving of "br" files (Brotli compression), HTTPS is required.

#### Create Certificate

Create a self-signed certificate and export it.

In PowerShell:
```
# Create the certificate in the Windows Certificate Store
$cert = New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "Cert:\CurrentUser\My" -KeyExportPolicy Exportable

# Set a temporary password for the export process
$pwd = ConvertTo-SecureString -String "password" -AsPlainText -Force

# Export as a PFX file (this contains both the key and the certificate)
Export-PfxCertificate -Cert $cert -FilePath "cert.pfx" -Password $pwd
```

#### Convert

Move the generated `.pfx` file to the scripts directory, and convert the generated `.pfx` file to a `.pem` usable in Python.

The "cryptography" module is required.
If missing, install it in the Python virtual environment:
```
pip install cryptography
```

In Python virtual environment, execute the conversion script:
```
python convert_ssl.py
```

> **NOTE:** Make sure the file name and password are set correctly (`pfx_path` and `pfx_password` variables at the beginning of the script).

---
## Usage

### Start Server

If not already done, start the virtual environment:
```
.\<ENV_NAME>\Scripts\activate
```

Launch the server:
```
python server_brotli.py --cert cert.pem --key key.pem --dir <PATH_TO_ROOT>
```
Where `<PATH_TO_ROOT>` is the directory containing the hosted files.
E.g.:
```
python server_brotli.py --cert cert.pem --key key.pem --dir D:\webserver\root
```

> **NOTE:** By default on port 4443, but can be changed using the `port` command line parameter.

### Browse

Acces the server at the following URL:
https://localhost:4443/

> **NOTE:** Security Warning.
> Because the certificate is "self-signed" (not issued by a trusted authority),
> the browser will show a "Your connection is not private" warning.
> Click "Advanced" and then "Proceed to localhost" to bypass it.

---
## Files

Scripts:
* `server_brotli.py`: Main Python script launching the server.
* `convert_ssl.py`: Utility Python script to convert the certificate to `.pem` files.
* `launch.bat': Shell script to launch the server from within the virtual environment directly.
	The script must be adapted!

Generated files:
* `cert.pfx`: Certificate generated in PowerShell.
* `cert.pem`: Certificate extracted from `.pfx` file.
* `key.pem`: Key extracted from `.pfx` file.
