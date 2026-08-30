import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.routes.building import get_db
from app.models.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"

engine = create_engine(
  SQLALCHEMY_DATABASE_URL,
  connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def client():
  return TestClient(app)

@pytest.fixture
def db():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)

  db = TestingSessionLocal()

  def override_get_db():
    yield db

  app.dependency_overrides[get_db] = override_get_db

  yield db

  db.close()
  app.dependency_overrides.clear()
