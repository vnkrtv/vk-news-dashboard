import app.app as application
import os
os.environ['HOST'] = '0.0.0.0'
os.environ['PORT'] = '8050'
application.app.run_server(debug=True)
