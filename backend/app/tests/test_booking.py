import pytest
from app.models.booking import Booking
from app.models.building import Building
from app.models.sauna import Sauna
from app.models.user import User
from datetime import datetime

@pytest.fixture
def building(db):
  building = Building(name="Viialan Kartano", address="Viialantie 999", duration_minutes=60)
  db.add(building)
  db.commit()
  db.refresh(building)

  return building

@pytest.fixture
def sauna(db, building):
  sauna = Sauna(name="A1", building_id=building.id)
  db.add(sauna)
  db.commit()
  db.refresh(sauna)

  return sauna

@pytest.fixture
def user(db, building, sauna):
  user = User(
    name="Erkki Esimerkki", 
    email="esimerkki@email.com",
    building_id=building.id,
    role="user"
  )

  db.add(user)
  db.commit()
  db.refresh(user)

  return user

#
# GET
#

def test_get_bookings(db, client, building, sauna, user):
  start_time = datetime(2026, 12, 6, 18, 0)
  end_time = datetime(2026, 12, 6, 19, 0)

  booking = Booking(
    start_time=start_time, 
    end_time=end_time, 
    status="confirmed", 
    building_id=building.id, 
    user_id=user.id, 
    sauna_id=sauna.id
  )
  db.add(booking)
  db.commit()

  response = client.get("/bookings")
  assert response.status_code == 200
  assert response.json()[0]["start_time"] == "2026-12-06T18:00:00"
  assert response.json()[0]["end_time"] == "2026-12-06T19:00:00"
  assert response.json()[0]["status"] == "confirmed"

def test_get_booking_by_id(db, client, building, sauna, user):
  start_time = datetime(2026, 12, 6, 18, 0)
  
  new_booking = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  booking_id = new_booking.json()["id"]

  response = client.get(f"/bookings/{booking_id}")
  assert response.status_code == 200
  assert datetime.fromisoformat(response.json()["start_time"]) == start_time
  assert response.json()["building"]["id"] == building.id
  assert response.json()["sauna"]["id"] == sauna.id
  assert response.json()["user"]["id"] == user.id

def test_booking_not_found(db, client):
  response = client.get("/bookings/23434234324")
  assert response.status_code == 404

#
# POST
#

def test_create_booking(db, client, building, sauna, user):
  start_time = datetime(2026, 12, 6, 18, 0)

  response = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  assert response.status_code == 200
  assert datetime.fromisoformat(response.json()["start_time"]) == start_time
  assert response.json()["building"]["id"] == building.id
  assert response.json()["sauna"]["id"] == sauna.id
  assert response.json()["user"]["id"] == user.id

def test_building_not_found(db,client, sauna, user):
  start_time = datetime(2026, 12, 6, 18, 0)
      
  response = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": 8747847457,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  assert response.status_code == 404

def test_sauna_not_found(db, client, building, user):
  start_time = datetime(2026, 12, 6, 18, 0)
      
  response = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": 47853445,
      "user_id": user.id
    }
  )

  assert response.status_code == 404

def test_sauna_does_not_match_building(db, client, building, user):
  other_building = client.post(
    "/buildings",
    json={
      "name": "Siuron taloyhtiö",
      "address": "Siurontie 666",
      "duration_minutes": 45
    }
  )

  other_building_id = other_building.json()["id"]

  sauna = client.post(
    "/saunas",
    json={
      "name": "B2",
      "building_id": other_building_id,
    }
  )

  sauna_id = sauna.json()["id"]
  
  start_time = datetime(2026, 12, 6, 18, 0)
        
  response = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna_id,
      "user_id": user.id
    }
  )

  assert response.status_code == 404

def test_overlapping_bookings(db, client, building, sauna, user):
  second_user = client.post(
    "/users",
    json={
      "name": "Jaska Jokunen",
      "email": "jaska@hotmail.com",
      "building_id": building.id,
      "role": "user"
    }
  )

  second_user_id = second_user.json()["id"]

  start_time = datetime(2026, 12, 6, 18, 0)
      
  first_booking = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  second_booking = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": second_user_id
    }
  )

  assert first_booking.status_code == 200
  assert second_booking.status_code == 400

def test_user_overlapping_sauna_booking(db, client, building, sauna, user):
  first_start_time = datetime(2026, 12, 6, 18, 0)
  second_start_time = datetime(2026, 12, 6, 18, 30)
        
  first_booking = client.post(
    "/bookings",
    json={
      "start_time": first_start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  second_booking = client.post(
    "/bookings",
    json={
      "start_time": second_start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  assert first_booking.status_code == 200
  assert second_booking.status_code == 400

#
# PUT
#

def test_update_booking(db, client, building, sauna, user):
  start_time = datetime(2026, 12, 6, 18, 0)
      
  booking = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  booking_id = booking.json()["id"]

  updated_start_time = datetime(2026, 12, 6, 19, 00)

  updated_booking = client.put(
    f"/bookings/{booking_id}",
    json={
      "start_time": updated_start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  assert booking.status_code == 200
  assert updated_booking.status_code == 200
  assert datetime.fromisoformat(updated_booking.json()["start_time"]) == updated_start_time


def test_update_booking_not_found(db, client, building, sauna, user):
  start_time = datetime(2026, 12, 6, 19, 00)
  
  response = client.put(
    "/bookings/343443242343",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  assert response.status_code == 404


def test_update_booking_building_not_found(db, building, client, sauna, user):
  start_time = datetime(2026, 12, 6, 18, 0)
        
  booking = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  booking_id = booking.json()["id"]

  updated_start_time = datetime(2026, 12, 6, 19, 00)

  updated_booking = client.put(
    f"/bookings/{booking_id}",
    json={
      "start_time": updated_start_time.isoformat(),
      "building_id": 8743678437864378,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  assert updated_booking.status_code == 404

def test_update_booking_sauna_not_found(db, building, client, sauna, user):
  start_time = datetime(2026, 12, 6, 18, 0)
        
  booking = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  booking_id = booking.json()["id"]

  updated_start_time = datetime(2026, 12, 6, 19, 00)

  updated_booking = client.put(
    f"/bookings/{booking_id}",
    json={
      "start_time": updated_start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": 783474378643,
      "user_id": user.id
    }
  )

  assert updated_booking.status_code == 404

#
# DELETE
#

def test_delete_booking_by_id(db, client, building, sauna, user):
  start_time = datetime(2026, 12, 6, 18, 0)
    
  new_booking = client.post(
    "/bookings",
    json={
      "start_time": start_time.isoformat(),
      "building_id": building.id,
      "sauna_id": sauna.id,
      "user_id": user.id
    }
  )

  booking_id = new_booking.json()["id"]

  response_delete = client.delete(f"/bookings/{booking_id}")
  assert response_delete.status_code == 204

  response_get = client.get(f"/bookings/{booking_id}")
  assert response_get.status_code == 404

def test_delete_booking_id_not_found(db, client):
  response = client.delete("/bookings/4353453")
  assert response.status_code == 404
