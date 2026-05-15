import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client for integration tests."""
    from app.main import app

    return TestClient(app)


@pytest.fixture
def client_no_raise() -> TestClient:
    """FastAPI test client that does not re-raise server exceptions.
    Used to test generic exception handlers, for example internal server errors."""
    from app.main import app

    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def valid_pdf_one() -> bytes:
    """Read the first valid PDF fixture as bytes."""
    with open("tests/fixtures/Doc1.pdf", "rb") as f:
        return f.read()


@pytest.fixture
def valid_pdf_two() -> bytes:
    """Read the second valid PDF fixture as bytes."""
    with open("tests/fixtures/Doc2.pdf", "rb") as f:
        return f.read()


@pytest.fixture
def valid_pdf_three() -> bytes:
    """Read the third valid PDF fixture as bytes."""
    with open("tests/fixtures/Doc3.pdf", "rb") as f:
        return f.read()


@pytest.fixture
def invalid_pdf() -> bytes:
    """Read the invalid PDF fixture (txt file) as bytes."""
    with open("tests/fixtures/Doc4-invalid.pdf", "rb") as f:
        return f.read()


@pytest.fixture
def empty_pdf() -> bytes:
    """Read the empty PDF fixture as bytes."""
    with open("tests/fixtures/Doc5-empty.pdf", "rb") as f:
        return f.read()
