from appflask import app
from flask import (
    jsonify
)


def configure_routes(app):
    @app.route('/')
    def greet():
        data = {"data": "Hello"}
        return (jsonify(data))


    @app.route('/test')
    def test():
        data = {"data": "Hello"}
        return (jsonify(data))