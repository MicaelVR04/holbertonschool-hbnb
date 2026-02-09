from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # This should be a User object
        self.amenities = []  # List of Amenity objects
        self.reviews = []    # List of Review objects

    def add_amenity(self, amenity):
        """Associate an amenity with this place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        """Add a review to this place."""
        self.reviews.append(review)
