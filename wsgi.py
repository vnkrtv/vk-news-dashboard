import app.app as application

app = application.app
server = application.server

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
