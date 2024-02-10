from appflask import app
from routes import configure_routes

configure_routes(app)

if __name__ == "__main__":
    app.run()