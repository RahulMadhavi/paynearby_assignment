import os
from flask_script import Manager
from app.main import create_app , socketio


app = create_app(os.getenv('FLASK_APP_ENV') or 'development')

# manager = Manager(app)

# @manager.command
def run():
    # socketio.run(app=app, host='0.0.0.0', port=8100)
    app.run(host='127.0.0.1', port=5200)
    

# app.app_context().push()

if __name__ == '__main__':
    # manager.run()
    run()