#from app.app import create_app

#app = create_app()
#if __name__ == '__main__':
#    app.run(debug=True)
    
import sys
import logging
import os
from subprocess import Popen

def main():
    log = logging.getLogger('werkzeug')
    log.disabled = True
    import app.models.wsgi as wsgi
    wsgi.main()
    #flasklistener.startlistener()

if __name__ == "__main__":
    main()

