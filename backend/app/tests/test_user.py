import pytest
from app.models.user import User
from app.models.building import Building

@pytest.fixture
def building(db):
  building = Building(name="Viialan Kartano", address="Viialantie 999", duration_minutes=60)
  db.add(building)
  db.commit()
  db.refresh(building)

  return building

def test_get_users(db, client, building):
  user = User(name="Maija Mehiläinen", email="maija.mehilainen@email.com", role="user", building_id=building.id)
  db.add(user)
  db.commit()

  response = client.get("/users")
  assert response.status_code == 200
  assert response.json()[0]["name"] == "Maija Mehiläinen"
  assert response.json()[0]["email"] == "maija.mehilainen@email.com"
  assert response.json()[0]["role"] == "user"

def test_create_user(db, client, building):
  response = client.post(
    "/users",
    json={
      "name": "Keijo Kekäläinen",
      "role": "user",
      "email": "keijokek85@hotmail.com",
      "building_id": building.id
    }
  )

  assert response.status_code == 200
  assert response.json()["name"] == "Keijo Kekäläinen"
  assert response.json()["email"] == "keijokek85@hotmail.com"
  assert response.json()["role"] == "user"
  assert response.json()["building"]["id"] == building.id

def test_get_user_by_id(db, client, building):
  new_user = client.post(
    "/users",
    json={
      "name": "Kaija Koo",
      "role": "user",
      "email": "kaijakoo@email.com",
      "building_id": building.id
    }
  )

  user_id = new_user.json()["id"]
  response = client.get(f"/users/{user_id}")
  
  assert response.status_code == 200
  assert response.json()["name"] == "Kaija Koo"
  assert response.json()["email"] == "kaijakoo@email.com"
  assert response.json()["role"] == "user"
  assert response.json()["building"]["id"] == building.id

def test_delete_user_by_id(db, client, building):
  new_user = client.post(
    "/users",
    json={
      "name": "Ella Mozzarella",
      "role": "user",
      "email": "ella01@email.com",
      "building_id": building.id
    }
  )

  user_id = new_user.json()["id"]

  response_delete = client.delete(f"/users/{user_id}")
  assert response_delete.status_code == 204

  response_get = client.get(f"/users/{user_id}")
  assert response_get.status_code == 404

def test_get_user_not_found(db, client):
  response = client.get("/users/2342342343")
  assert response.status_code == 404

def test_delete_user_not_found(db, client):
  response = client.delete("/users/23432423432")
  assert response.status_code == 404

def test_create_user_building_not_found(db, client):
  response = client.post(
    "/users",
    json={
      "name": "Kaisa Kak",
      "role": "user",
      "email": "kakkak@email.com",
      "building_id": 8888888888
    }
  )

  assert response.status_code == 404

def test_duplicate_user_email(db, client, building):
  user1 = client.post(
    "/users",
    json={
      "name": "Jaana Jokunen",
      "role": "user",
      "email": "jaana111@email.com",
      "building_id": building.id
    }
  )

  user2 = client.post(
    "/users",
    json={
      "name": "Jaana Jokunen",
      "role": "user",
      "email": "jaana111@email.com",
      "building_id": user1.json()["building"]["id"]
    }
  )

  assert user2.status_code == 404
