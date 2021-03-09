from src import app
from src import config

app = app.app
server = app.server

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=config.DEBUG)
