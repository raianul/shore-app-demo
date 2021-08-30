from datetime import datetime
from sqlalchemy import Column

from shore_app.extensions import db
from shore_app.utils import get_current_time, Serializer
from shore_app.config import STRING_LEN


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
        user = Serializer.serialize(self)
        if 'subscriptions' in user:
            del user['subscriptions']
        if 'products' in user:
            del user['products']
        return user

    def valid_subs_for_alert(self):
        now = datetime.utcnow()
        subs = []
        for sub in self.subscriptions:
            interval = (now - sub.last_email_sent).total_seconds() / 60.0
            if interval >= sub.interval:
                subs.append(sub)
        return subs
