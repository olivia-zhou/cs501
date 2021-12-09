#from app.app import create_app

#app = create_app()
#if __name__ == '__main__':
#    app.run(debug=True)
    
import sys
import logging
import os
from subprocess import Popen

import app.models.wsgi as wsgi

def main():
    log = logging.getLogger('werkzeug')
    log.disabled = True
    wsgi.main()

if __name__ == "__main__":
    main()

