#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import click
from flask.cli import FlaskGroup

from pontos.ext import configuration, api
from pontos.services import usuarios_services


def create_app(info):

    app = api.create_api_app()
    configuration.init_app(app)
    configuration.load_extensions(app)
    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """This is a management script for the aseg application."""


@cli.command()
@click.option("--nome", prompt=True, required=True)
@click.option("--fone", prompt=True, required=True)
@click.option("--email", prompt=True, required=True)
@click.option("--perfil", prompt=True, required=True, default="gerente")
@click.option("--empresa_id", prompt=True, required=False, default=None)
@click.password_option(help="Password.")
def criar_usuario(nome, fone, email, perfil, empresa_id, password):
    """Criar novo usuário."""

    novo_usuario = usuarios_services.criar_usuario(
        nome_completo=nome, fone=fone, email=email, password=password, perfil=perfil, empresa_id=empresa_id
    )

    print(json.dumps(novo_usuario, indent=2))


if __name__ == "__main__":
    cli()