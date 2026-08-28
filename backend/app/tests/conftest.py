from sqlalchemy import create_engine

SQL_ALCHEMY_TEST_DATABASE_ENGINE_URL = "sqlite:///./test_database.db"

engine = create_engine(
  SQL_ALCHEMY_TEST_DATABASE_ENGINE_URL,
  connect_args={"check_same_thread": False}
)
