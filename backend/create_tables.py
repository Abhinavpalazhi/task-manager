from database import engine
from models.task import Task
from models.user import User
from models.refresh_token import RefreshToken

User.metadata.create_all(bind=engine)
Task.metadata.create_all(bind=engine)
RefreshToken.metadata.create_all(bind=engine)
