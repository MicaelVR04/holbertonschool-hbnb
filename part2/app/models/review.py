from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        self.text = text
        self.rating = rating
        self.place = place  # This should be a Place object
        self.user = user    # This should be a User object
