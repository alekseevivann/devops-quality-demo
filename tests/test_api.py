def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_sum_ok(client):
    response = client.get("/api/sum?a=2&b=3.5")
    assert response.status_code == 200
    assert response.get_json()["result"] == 5.5


def test_sum_bad_params(client):
    assert client.get("/api/sum?a=2").status_code == 400
    assert client.get("/api/sum?a=x&b=1").status_code == 400


def test_create_and_list_tasks(client):
    created = client.post("/api/tasks", json={"title": "Проверить конвейер"})
    assert created.status_code == 201
    listing = client.get("/api/tasks").get_json()
    assert [t["title"] for t in listing] == ["Проверить конвейер"]


def test_create_task_validation(client):
    assert client.post("/api/tasks", json={"title": ""}).status_code == 400
    assert client.post("/api/tasks", data="не json").status_code == 400


def test_complete_task(client):
    task = client.post("/api/tasks", json={"title": "Задача"}).get_json()
    done = client.post(f"/api/tasks/{task['id']}/done")
    assert done.status_code == 200
    assert done.get_json()["done"] is True


def test_complete_missing_task(client):
    assert client.post("/api/tasks/999/done").status_code == 404
