from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        
        # Validation
        if not title or not description:
            raise ValueError("Title and description are required")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
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
