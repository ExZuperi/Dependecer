import argparse
import os
import socket
import ssl
import netifaces

import PoCGenerator
import SSLCertificate
import DataHandler
import ServerSide


def hello_logo():
    print("""        
     _____       _____                      _ 
    |   __| _ _ |__   | _ _  ___  ___  ___ |_|
    |   __||_'_||   __|| | || . || -_||  _|| |
    |_____||_,_||_____||___||  _||___||_|  |_|
    t.me/ExZuperi           |_|               
    github.com/ExZuperi
    """)


if __name__ == "__main__":
    cert_file = ""
    key_file = ""
    parser = argparse.ArgumentParser(
        description='Project to handle requests from malicious PoC of Dependency Confusion or Similar Name packages. '
                    'Also can be used to generate those packages (gem, npm, pip).')

    parser.add_argument('-s', '--ssl', help='Enable SSL option, can be true or false if anything other than "True"',
                        required=True, type=str)
    parser.add_argument('-i', '--interface',
                        help="Interface's name where server will be started. Default is lo (localhost)", required=False,
                        type=str, default="lo")
    parser.add_argument('-p', '--port', help='Change server port. Default is 449', required=False, type=int,
                        default=449)
    parser.add_argument('-cn', '--common_name', help='Common Name for the certificate. If this argument provided, will generate self-signed certificate',
                        required=False, type=str)
    parser.add_argument('-c', '--cert_file', help='Path to a public certificate file', required=False, type=str)
    parser.add_argument('-k', '--key_file', help='Path to a private key file', required=False, type=str)
    parser.add_argument('-poc', '--poc_name', help='Name of malicious package. Creates directory with malicious packages. '
                                                   'Example: --poc android-x64', required=False, type=str)
    parser.add_argument('-is', '--ignore_server', help="Don't start server that will handle connections. Can be useful when you create a lot of packages", required=False, action="store_true")

    args = parser.parse_args()

    ssl_enabled = str(args.ssl).lower() == "true"

    if ssl_enabled:
        if (((args.cert_file is None) and (args.key_file is None)) and (args.common_name is None)) and args.ignore_server is not None:
            parser.error("When SSL is enabled, both --cert_file and --key_file arguments are required or common name should be provided to create those files.")

    if args.interface:
        try:
            netifaces.ifaddresses(args.interface)
        except Exception as e:
            print(e)
            parser.error("Can't find interface or it's busy")

    if args.port:
        try:
            host_ip = netifaces.ifaddresses(args.interface)[netifaces.AF_INET][0]['addr']
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host_ip, args.port))
            sock.close()
            if result == 0:
                parser.error("Port should be free.")
        except:
            parser.error("Can't find interface, no IP or it's busy")

    if args.common_name and ssl_enabled:
        SSLCertificate.create_self_signed_cert(args.common_name)
        cert_file = f"./certificates/{args.common_name}.crt"
        key_file = f"./certificates/{args.common_name}.key"

    if args.cert_file is not None and args.key_file is not None and ssl_enabled:
        cert_file = args.cert_file
        key_file = args.key_file

    if args.poc_name:
        PoCGenerator.generate_packets_of_shit(args.poc_name, host_ip, args.port, ssl_enabled)

    hello_logo()
    DataHandler.mark_new_file() if not os.path.exists("access.log") else None
    try:
        if not args.ignore_server:
            ServerSide.start_server(True, host_ip, args.port, cert_file=cert_file, key_file=key_file) if ssl_enabled else ServerSide.start_server(False, host_ip, args.port)
    except ssl.SSLError:
        parser.error("Certificates are not valid. SSL Parse error")
