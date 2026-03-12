from flask_bcrypt import generate_password_hash, check_password_hash
from app.models.base_model import BaseModel, db


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    places = db.relationship("Place", back_populates="owner", cascade="all, delete-orphan", lazy=True)
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan", lazy=True)

    def hash_password(self, password):
        self.password = generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return check_password_hash(self.password, password)
