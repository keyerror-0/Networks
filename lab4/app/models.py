from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

item_category = db.Table(
    'item_category',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    items: so.Mapped[list['Item']] = so.relationship(secondary=item_category, back_populates='categories', lazy='dynamic')

class Item(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    price: so.Mapped[int] = so.mapped_column(index=True)
    old_price: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    currency: so.Mapped[str] = so.mapped_column(sa.CHAR)
    href: so.Mapped[str] = so.mapped_column(sa.String(160), unique=True)
    categories: so.Mapped[list['Category']] = so.relationship(
        secondary=item_category, 
        back_populates='items',
        lazy='dynamic'
    )

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'old_price': self.old_price,
            'currency': self.currency,
            'href': self.href,
            'categories': [c.name for c in self.categories]
        }
