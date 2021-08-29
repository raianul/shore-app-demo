from sqlalchemy import Column

from shore_app.extensions import db
from shore_app.utils import get_current_time, Serializer
from shore_app.constants import STRING_LEN


class User(db.Model, Serializer):

    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False)
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    subscribe = Column(db.Boolean, default=True, nullable=False)
    create_at = Column(db.DateTime, nullable=False, default=get_current_time)
    update_at = Column(db.DateTime, onupdate=get_current_time)
    subscriptions = db.relationship('Subscription', backref=db.backref('user', lazy='joined'),
                                    lazy='selectin', cascade="all, delete-orphan")

    def serialize(self):
        return Serializer.serialize(self)
