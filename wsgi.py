import app.app as application
import app.config as cfg

app = application.app
server = application.server

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=cfg.DEBUG)
