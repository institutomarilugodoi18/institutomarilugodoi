import pytest

# ===== FIXTURES =====

# Desabilita redirecionamento SSL durante os testes para evitar falhas de redirecionamento.
@pytest.fixture(autouse=True)
def desabilita_ssl_redirect(settings):
    settings.SECURE_SSL_REDIRECT = False