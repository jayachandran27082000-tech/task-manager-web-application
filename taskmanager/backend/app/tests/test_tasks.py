def test_create_task(client, auth_headers):
    response = client.post("/tasks", json={
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["completed"] is False


def test_create_task_unauthenticated(client):
    response = client.post("/tasks", json={"title": "Test"})
    assert response.status_code == 401


def test_list_tasks(client, auth_headers):
    client.post("/tasks", json={"title": "Task 1"}, headers=auth_headers)
    client.post("/tasks", json={"title": "Task 2"}, headers=auth_headers)
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["tasks"]) == 2


def test_list_tasks_filter_completed(client, auth_headers):
    r1 = client.post("/tasks", json={"title": "Task 1"}, headers=auth_headers)
    client.put(f"/tasks/{r1.json()['id']}", json={"completed": True}, headers=auth_headers)
    client.post("/tasks", json={"title": "Task 2"}, headers=auth_headers)

    response = client.get("/tasks?completed=true", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["tasks"][0]["completed"] is True


def test_list_tasks_pagination(client, auth_headers):
    for i in range(5):
        client.post("/tasks", json={"title": f"Task {i}"}, headers=auth_headers)

    response = client.get("/tasks?page=1&page_size=3", headers=auth_headers)
    data = response.json()
    assert len(data["tasks"]) == 3
    assert data["total"] == 5
    assert data["total_pages"] == 2


def test_get_task(client, auth_headers):
    create_r = client.post("/tasks", json={"title": "My Task"}, headers=auth_headers)
    task_id = create_r.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "My Task"


def test_get_task_not_found(client, auth_headers):
    response = client.get("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_task(client, auth_headers):
    create_r = client.post("/tasks", json={"title": "Old Title"}, headers=auth_headers)
    task_id = create_r.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "New Title", "completed": True}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["completed"] is True


def test_delete_task(client, auth_headers):
    create_r = client.post("/tasks", json={"title": "Delete Me"}, headers=auth_headers)
    task_id = create_r.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    get_r = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_r.status_code == 404


def test_cannot_access_other_users_tasks(client):
    # Register two users
    client.post("/register", json={"username": "user1", "email": "u1@test.com", "password": "pass1234"})
    client.post("/register", json={"username": "user2", "email": "u2@test.com", "password": "pass1234"})

    token1 = client.post("/login", json={"username": "user1", "password": "pass1234"}).json()["access_token"]
    token2 = client.post("/login", json={"username": "user2", "password": "pass1234"}).json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    task_r = client.post("/tasks", json={"title": "User1 private task"}, headers=headers1)
    task_id = task_r.json()["id"]

    # User2 should not be able to access user1's task
    response = client.get(f"/tasks/{task_id}", headers=headers2)
    assert response.status_code == 404
