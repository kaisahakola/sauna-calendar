from app.models.sauna import Sauna
from app.models.building import Building

def test_get_saunas(db, client):
  building = Building(name="Viialan Kartano", address="Viialantie 666")
  db.add(building)
  db.commit()
  db.refresh(building)

  sauna = Sauna(name="A1", building_id=building.id)
  db.add(sauna)
  db.commit()

  response = client.get("/saunas")
  assert response.status_code == 200
  assert response.json()["name"] == "A1"
