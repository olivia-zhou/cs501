"""What should this thing do"""
# from Guinicorn documentation
# https://docs.gunicorn.org/en/latest/custom.html
import multiprocessing
import gunicorn.app.base
# from flask import Flask, render_template, make_response, request, Response
# from app.models.listener import FlaskListener
from app.models.listener import app


def number_of_workers():
    """Returns the number of workers you may spawn"""
    return (multiprocessing.cpu_count() * 2) + 1


class GunicornWSGI(gunicorn.app.base.BaseApplication):
    """I am unsure of what to put here"""
    def __init__(self, myApp, options=None):
        self.options = options or {}
        self.application = myApp
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    """What should I put here"""
    options = {
        'bind': "0.0.0.0:8080",
        'workers': number_of_workers(),
    }
    GunicornWSGI(app, options).run()


if __name__ == '__main__':
    main()
