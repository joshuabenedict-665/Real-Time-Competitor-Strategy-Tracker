# drop_create.py
from database import engine, Base
from models import MyProduct, CompetitorData

# Drop existing tables
Base.metadata.drop_all(bind=engine)

# Create tables with new schema (including `image`)
Base.metadata.create_all(bind=engine)

print("Tables recreated with `image` column!")
