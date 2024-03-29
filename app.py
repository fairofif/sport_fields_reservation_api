from appflask import app
from routes import configure_routes
from routes_auth_player import player_auth_configure_routes
from routes_device import device_configure_routes
from routes_auth_admin import admin_auth_configure_routes
from routes_field_management import field_management_configure_routes
from routes_auth_relogin import relogin_configure_routes

device_configure_routes(app)
configure_routes(app)
player_auth_configure_routes(app)
admin_auth_configure_routes(app)
field_management_configure_routes(app)
relogin_configure_routes(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
