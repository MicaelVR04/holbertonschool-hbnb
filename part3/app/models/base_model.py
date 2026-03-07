import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base class for all models in the HBnB project."""
    __abstract__ = True

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save the object to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update attributes and save."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
