from app.models.base_model import BaseModel, db
from app import bcrypt


class User(BaseModel):
    """User model."""

    __tablename__ = "users"

    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    places = db.relationship("Place", backref="owner", lazy=True)
    reviews = db.relationship("Review", backref="author", lazy=True)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verifies if provided password matches hashed password."""
        return bcrypt.check_password_hash(self.password, password)
