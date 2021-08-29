from sqlalchemy import Column

from shore_app.extensions import db
from sqlalchemy.schema import ForeignKeyConstraint, UniqueConstraint
from shore_app.utils import get_current_time, Serializer, commit_or_rollback
from shore_app.constants import STRING_LEN


user_products = db.Table(
    'user_products',
    db.Column('user_id', db.Integer,
              db.ForeignKey('users.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
    UniqueConstraint('user_id', 'product_id', name='unique_user_product')
)


class Product(db.Model, Serializer):

    __tablename__ = 'products'

    id = Column(db.Integer, primary_key=True)
    phrases = Column(db.String(STRING_LEN), nullable=False)
    title = Column(db.String(STRING_LEN), nullable=False)
    item_id = Column(db.String(STRING_LEN), nullable=False)
    end_time = Column(db.DateTime)
    price = Column(db.Float(10, 2))
    last_price = Column(db.Float(10, 2))
    currency = Column(db.String(STRING_LEN))
    users = db.relationship('User', secondary=user_products,
                            backref='products', lazy='dynamic')

    def serialize(self):
        product = Serializer.serialize(self)
        if 'users' in product:
            del product['users']
        return product

    @staticmethod
    def get_or_create(**kwargs):
        defaults = kwargs.pop('defaults', {})
        product = Product.query.filter_by(**kwargs).first()
        created = True
        if product:
            created = False
        else:
            if defaults:
                kwargs.update(defaults)
            product = Product(**kwargs)
            db.session.add(product)
            commit_or_rollback(db.session)

        return product, created
