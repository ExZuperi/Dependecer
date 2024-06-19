import ssl
from flask import Flask, request, jsonify
from flask_cors import CORS

import DataHandler

app = Flask(__name__)
CORS(app)


@app.route('/PoC', methods=['POST'])
def handle_post():
    try:
        data = request.get_json()
        if not (
                "hostname" in data and "pwd" in data and "user" in data and "package_name" in data): return "Bad joke", 418

        external_ip = request.remote_addr

        if len(data["hostname"]) > 150 or len(data["pwd"]) > 500 or len(data["user"]) > 150 or len(data["package_name"]) > 100:
            print(data)
            return "Can't handle your data, too long, sorry. But I record it!", 413

        if DataHandler.collect_data(external_ip, data["hostname"], data["pwd"], data["user"], data["package_name"]):
            return "Data received and saved.", 200
        else:
            return "Something went wrong", 500
    except Exception as e:
        return "Use json format", 415


@app.errorhandler(404)
def page_not_found():
    return jsonify({'error': 'Not found', 'message': 'Thanks for BugBounty cooperation'}), 404


def start_server(ssl_enabled: bool, host_ip: str, port: int, cert_file="None", key_file="None"):
    if ssl_enabled:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(f'{cert_file}',
                                f'{key_file}')
        try:
            app.run(debug=False, host=f'{host_ip}', port=port, ssl_context=context, use_reloader=False, threaded=True)
        except ssl.SSLEOFError as e:
            print(e)
    else:
        app.run(debug=False, host=f'{host_ip}', port=port, use_reloader=False, threaded=True)