# Dependecer
Project to handle requests from malicious PoC of Dependency Confusion or Similar Name packages. Also can be used to generate those packages (gem, npm, pip).

# Installation instructions
Will clone project, goto it's directory and install all requirements
```
git clone https://github.com/ExZuperi/Dependecer.git && cd Dependecer && pip install -r requirements.txt
```

# Usage
```
usage: main.py [-h] -s SSL [-i INTERFACE] [-p PORT] [-cn COMMON_NAME] [-c CERT_FILE] [-k KEY_FILE] [-poc POC_NAME] [-is]

options:
  -h, --help
                        show this help message and exit

  -s SSL, --ssl SSL
                        Enable SSL option, can be true or false if anything other than "True"

  -i INTERFACE, --interface INTERFACE
                        Interface's name where server will be started. Default is lo (localhost)

  -p PORT, --port PORT
                        Change server port. Default is 449

  -cn COMMON_NAME, --common_name COMMON_NAME
                        Common Name for the certificate. If this argument provided, will generate self-signed certificate

  -c CERT_FILE, --cert_file CERT_FILE
                        Path to a public certificate file

  -k KEY_FILE, --key_file KEY_FILE
                        Path to a private key file

  -poc POC_NAME, --poc_name POC_NAME
                        Name of malicious package. Creates directory with malicious packages. Example: --poc android-x64

  -is, --ignore_server
                        Don't start server that will handle connections. Can be useful when you create a lot of packages
```

# Examples
## Recommended method
Use existing certificates and secret key files, use interface wlan0, use port 449, use https communication. Also will generate malicious packages with "android-x64" name that communicates over https.
```
python3 main.py -s True -c /etc/letsencrypt/live/mysite.com/fullchain.pem -k /etc/letsencrypt/live/mysite.com/privkey.pem -i wlan0 -p 449 -poc android-x64
```

## Recommended method 2
Generate self-signed certificate, use interface wlan0, use port 449, use https communications. Also generate malicious packages with "android-x64" name that communicates over https.
```
python3 main.py -s True -cn test.cert.com -i wlan0 -p 449 -poc android-x64
```

## Only generate malicious packages
Will generate malicious code that works over https, with wlan0 IP, 2222 port and "some" name. Server won't be running 
```
python3 main.py -s True -i wlan0 -p 2222 -poc some -is
```

## Communication over http
Can cause security issues
Use interface wlan0, use port 2222, use http communications. Also generate malicious packages with "android-x64" name that communicates over http.
```
python3 main.py -s BLABLABLA -i wlan0 -p 2222 -poc android-x64
```

