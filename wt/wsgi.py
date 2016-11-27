from werkzeug.wsgi import DispatcherMiddleware
from wt import dashboard, adapter

application = DispatcherMiddleware(dashboard.create_app(config_name="production"), {
    '/go': adapter.create_app(config_name="production")
})