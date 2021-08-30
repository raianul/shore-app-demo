from datetime import datetime
from sqlalchemy import Column


from shore_app.extensions import db
from shore_app.utils import get_current_time, Serializer
from shore_app.constants import STRING_LEN, ALERT_INTERVAL


class Subscription(db.Model, Serializer):

    __tablename__ = 'subscriptions'

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, db.ForeignKey('users.id'),
                     nullable=False)
    phrases = Column(db.String(STRING_LEN), nullable=False)
    interval = Column(db.Integer, nullable=False)
    last_email_sent = db.Column(
        db.DateTime, index=True, default=get_current_time)
    active = Column(db.Boolean, default=True, nullable=False)
    create_at = Column(db.DateTime, nullable=False, default=get_current_time)
    update_at = Column(db.DateTime, onupdate=get_current_time)

    def serialize(self):
        sub = Serializer.serialize(self)
        if 'user' in sub:
            del sub['user']
        if 'products' in sub:
            del sub['products']
        return sub

    @property
    def valid_for_email(self):
        now = datetime.utcnow()
        interval = (now - self.last_email_sent).total_seconds() / 60.0
        if interval >= self.interval:
            return True
        return False
