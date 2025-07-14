from app import app, get_app

CONFIG_SERVER_URL = '127.0.0.1'
CONFIG_SERVER_PORT = '5005'
CONFIG_SSL_CERT = "../certificate/certificate.crt"
CONFIG_SSL_KEY = "../certificate/private.key"
CONFIG_THREADED = True
CONFIG_DEBUG = True

if __name__ == '__main__':
    a = get_app()
    #a.run(debug=False, host='0.0.0.0', port=10000)
    a.run(host=CONFIG_SERVER_URL, port=int(CONFIG_SERVER_PORT), debug=CONFIG_DEBUG, threaded=CONFIG_THREADED)
