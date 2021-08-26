from sqlalchemy import Column

from shore_app.extensions import db
from shore_app.utils import get_current_time
from shore_app.constants import STRING_LEN


class User(db.Model):

    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False)
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    subscribe = Column(db.Boolean, default=True, nullable=False)
    create_at = Column(db.DateTime, nullable=False, default=get_current_time)
    update_at = Column(db.DateTime, onupdate=get_current_time)
