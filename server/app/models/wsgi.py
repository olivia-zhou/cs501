#from Guinicorn documentation (https://docs.gunicorn.org/en/latest/custom.html)
import multiprocessing
import gunicorn.app.base
from flask import Flask, render_template, make_response, request, Response
from listner import FlaskListener
#from testing import testclass

test = FlaskListener()
app = test.getapp() 

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class GunicornWSGI(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers(),
    }
    GunicornWSGI(app, options).run()