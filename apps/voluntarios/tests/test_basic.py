import pytest

def test_pytest_setup():
    """Verifica se o ambiente de teste está funcionando"""
    assert True

@pytest.mark.django_db
def test_django_setup(client):
    """Verifica se o Django está integrado ao Pytest"""
    response = client.get('/')
    # Este teste passará se sua home retornar 200 ou 404 (o importante é o Django responder)
    assert response.status_code in [200, 404]