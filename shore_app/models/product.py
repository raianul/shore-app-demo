from sqlalchemy import Column

import timeago

from shore_app.extensions import db
from sqlalchemy.schema import UniqueConstraint
from shore_app.utils import get_current_time, Serializer, commit_or_rollback
from shore_app.config import STRING_LEN


subs_products = db.Table(
    'subs_products',
    db.Column('subscription_id', db.Integer,
              db.ForeignKey('subscriptions.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
    UniqueConstraint('subscription_id', 'product_id',
                     name='unique_user_product')
)


class Product(db.Model, Serializer):

    __tablename__ = 'products'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(STRING_LEN), nullable=False)
    item_id = Column(db.String(STRING_LEN), nullable=False)
    link = Column(db.String(STRING_LEN))
    end_time = Column(db.DateTime)
    price = Column(db.Float(precision=2))
    last_price = Column(db.Float(precision=2))
    currency = Column(db.String(STRING_LEN))
    create_at = Column(db.DateTime, nullable=False, default=get_current_time)
    update_at = Column(db.DateTime, onupdate=get_current_time)
    subscriptions = db.relationship('Subscription', secondary=subs_products,
                                    backref='products', lazy='dynamic')

    def serialize(self):
        product = Serializer.serialize(self)
        product.update(self.price_variation)
        if 'subscriptions' in product:
            del product['subscriptions']
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

    @property
    def price_variation(self):
        diff = timeago.format(self.create_at, self.update_at)
        if not self.price or not self.last_price:
            return {}

        if self.price < self.last_price:
            return {
                'diff': diff,
                'percentage': round((self.last_price - self.price) * 100 / self.price),
                'mode': 'Decrease'
            }
        elif self.price > self.last_price:
            return {
                'diff': diff,
                'percentage': round((self.price - self.last_price) * 100 / self.price),
                'mode': 'Increase'
            }
        else:
            return {
                'diff': diff,
                'percentage': 0,
                'mode': 'Unchange'
            }

    @staticmethod
    def product_insights(products):
        products = Product.serialize_list(products)
        decrease_products = list(
            filter(lambda prodcut: prodcut['mode'] == 'Decrease' and prodcut['diff'] != 'just now', products))
        unchange_products = list(
            filter(lambda prodcut: prodcut['mode'] == 'Unchange' and prodcut['diff'] != 'just now', products))
        cheaper_product = min(products, key=lambda x: x['price'])

        return {
            'products': products,
            'decrease_products': decrease_products,
            'unchange_products': unchange_products,
            'cheaper_product': cheaper_product
        }
