from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ Use correct URL format (update with your credentials)
DATABASE_URL = "postgresql://postgres:Rex%404115@localhost:5433/smart-cloud"

# ❌ Remove check_same_thread (only used in SQLite)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
