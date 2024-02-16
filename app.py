from appflask import app
from routes import configure_routes
from routes_auth_player import player_auth_configure_routes

configure_routes(app)
player_auth_configure_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)