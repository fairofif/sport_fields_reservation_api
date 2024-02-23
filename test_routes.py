from app import app

def test_swagger_success():
    client = app.test_client()
    url = '/api/docs/#/'
    response = client.get(url)
    assert response.status_code == 200