from .database import engine, Base

from monolith import *

Base.metadata.create_all(bind=engine)