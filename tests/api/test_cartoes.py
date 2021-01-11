import mock


@mock.patch("pontos.services.cartoes_services.listar_cartoes")
def test_listar_todos_cartoes(listar_cartoes_mock, client):

    listar_cartoes_mock.return_value = [
        {
            "empresa_id": 1,
            "id": 3,
            "pontos": 0,
            "programa_id": 1,
            "usuario": {
                "avatar": "https://example.com/ze_thumb.png",
                "criado_em": "2021-01-11T18:20:41+00:00",
                "email": "ze@example.com",
                "fone": "12991000111",
                "id": 1,
                "nome_completo": "Ze Silva",
            },
        }
    ]

    response = client.get("/api/cartao")

    assert response.status_code == 200
