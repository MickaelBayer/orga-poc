from datetime import datetime

from src import db


class Organisation(db.Model):

    __tablename__ = "organisations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_on = db.Column(db.DateTime, nullable=False)
    can_have_children = db.Column(db.Boolean, nullable=False, default=True)
    parent_orga_id = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, name, description=None, can_have_children=True, parent_orga_id=1):
        self.name = name
        self.description = description
        self.can_have_children = can_have_children
        self.parent_orga_id = parent_orga_id
        self.created_on = datetime.now()

    def __repr__(self):
        return f"<name {self.name}>"
