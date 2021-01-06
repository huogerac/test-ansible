from pontos.ext import configuration, api


def create_app(**config):

    app = api.create_api_app()
    configuration.init_app(app, **config)
    configuration.load_extensions(app)
    return app
