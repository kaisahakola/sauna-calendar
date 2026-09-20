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

#
# GET
#

def test_get_users(db, client, building):
  user = User(name="Maija Mehiläinen", email="maija.mehilainen@email.com", building_id=building.id)
  db.add(user)
  db.commit()

  response = client.get("/users")
  assert response.status_code == 200
  assert response.json()[0]["name"] == "Maija Mehiläinen"
  assert response.json()[0]["email"] == "maija.mehilainen@email.com"

def test_get_user_by_id(db, client, building):
  new_user = client.post(
    "/users",
    json={
      "name": "Kaija Koo",
      "email": "kaijakoo@email.com",
      "building_id": building.id
    }
  )

  user_id = new_user.json()["id"]
  response = client.get(f"/users/{user_id}")
  
  assert response.status_code == 200
  assert response.json()["name"] == "Kaija Koo"
  assert response.json()["email"] == "kaijakoo@email.com"
  assert response.json()["building"]["id"] == building.id

def test_get_user_not_found(db, client):
  response = client.get("/users/2342342343")
  assert response.status_code == 404

#
# POST
#

def test_create_user(db, client, building):
  response = client.post(
    "/users",
    json={
      "name": "Keijo Kekäläinen",
      "email": "keijokek85@hotmail.com",
      "building_id": building.id
    }
  )

  assert response.status_code == 200
  assert response.json()["name"] == "Keijo Kekäläinen"
  assert response.json()["email"] == "keijokek85@hotmail.com"
  assert response.json()["building"]["id"] == building.id

def test_create_user_building_not_found(db, client):
  response = client.post(
    "/users",
    json={
      "name": "Kaisa Kak",
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
      "email": "jaana111@email.com",
      "building_id": building.id
    }
  )

  user2 = client.post(
    "/users",
    json={
      "name": "Jaana Jokunen",
      "email": "jaana111@email.com",
      "building_id": user1.json()["building"]["id"]
    }
  )

  assert user2.status_code == 404

#
# PUT
#

def test_update_user(db, client, building):
  user = client.post(
    "/users",
    json={
      "name": "Keijo Kekäläinen",
      "email": "keijokek85@hotmail.com",
      "building_id": building.id
    }
  )

  user_id = user.json()["id"]

  updated_user = client.put(
    f"/users/{user_id}",
    json={
      "name": "Kaija Kekäläinen",
      "email": "korkkaritkattoon@gmail.com",
      "building_id": building.id
    }
  )

  assert updated_user.status_code == 200
  assert updated_user.json()["name"] == "Kaija Kekäläinen"
  assert updated_user.json()["email"] == "korkkaritkattoon@gmail.com"

def test_update_user_not_foun(db, client, building):
  response = client.put(
    "/users/34324234",
    json={
      "name": "Kaija Kekäläinen",
      "email": "korkkaritkattoon@gmail.com",
      "building_id": building.id
    }
  )

  assert response.status_code == 404

def test_update_user_building_not_foun(db, client, building):
  user = client.post(
      "/users",
      json={
        "name": "Keijo Kekäläinen",
        "email": "keijokek85@hotmail.com",
        "building_id": building.id
      }
    )
  
  user_id = user.json()["id"]

  updated_user = client.put(
    f"/users/{user_id}",
    json={
      "name": "Kaija Kekäläinen",
      "email": "korkkaritkattoon@gmail.com",
      "building_id": 78667432786423
    }
  )

  assert updated_user.status_code == 404

#
# DELETE
#

def test_delete_user_by_id(db, client, building):
  new_user = client.post(
    "/users",
    json={
      "name": "Ella Mozzarella",
      "email": "ella01@email.com",
      "building_id": building.id
    }
  )

  user_id = new_user.json()["id"]

  response_delete = client.delete(f"/users/{user_id}")
  assert response_delete.status_code == 204

  response_get = client.get(f"/users/{user_id}")
  assert response_get.status_code == 404

def test_delete_user_not_found(db, client):
  response = client.delete("/users/23432423432")
  assert response.status_code == 404
