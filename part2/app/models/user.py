from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        # Basic validation
        if not email or "@" not in email:
            raise ValueError("Invalid email address")
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List of places owned by this user
        self.reviews = [] # List of reviews written by this user
