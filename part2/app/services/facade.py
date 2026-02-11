"""
Facade Pattern Implementation
The Facade simplifies interaction between the API and data layers.
It contains all business logic and validation rules.
"""

from app.persistence.repository import Repository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """
    Facade class that acts as a single entry point for the API.
    
    Benefits:
    - API only talks to Facade, not directly to Repository
    - All business logic is centralized here
    - Easy to add validations, logging, etc.
    - Clean interface for the Presentation layer
    """
    
    def __init__(self):
        # Initialize the repository (in-memory storage)
        self.repository = Repository()

    # ==================== USER OPERATIONS ====================
    
    def create_user(self, user_data):
        """
        Create a new user.
        
        Args:
            user_data: Dictionary with 'first_name', 'last_name', 'email'
        
        Returns:
            The newly created User object
        """
        # Create a new User instance with provided data
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email']
        )
        
        # Store it in the repository
        self.repository.add(new_user)
        
        return new_user

    def get_user_by_email(self, email):
        """
        Find a user by their email address.
        
        Args:
            email: The email to search for
        
        Returns:
            The User object if found, None otherwise
        """
        return self.repository.find_by_attribute('User', 'email', email)

    def get_user(self, user_id):
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: The ID of the user
        
        Returns:
            The User object if found, None otherwise
        """
        return self.repository.get(user_id, 'User')

    def get_all_users(self):
        """
        Retrieve all users.
        
        Returns:
            A list of all User objects
        """
        return self.repository.get_all('User')

    def update_user(self, user_id, user_data):
        """
        Update an existing user.
        
        Args:
            user_id: The ID of the user to update
            user_data: Dictionary with fields to update
        
        Returns:
            The updated User object, or None if not found
        """
        user = self.repository.get(user_id, 'User')
        if not user:
            return None
        
        # Update the user object with provided data
        user.update(user_data)
        
        # Save changes to the repository
        self.repository.update(user)
        
        return user

    # ==================== PLACE OPERATIONS ====================
    
    def create_place(self, place_data):
        """
        Create a new place.
        
        Args:
            place_data: Dictionary with place details and owner_id
        
        Returns:
            The newly created Place object
        """
        # Verify the owner (user) exists
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            return None
        
        new_place = Place(
            title=place_data['title'],
            description=place_data['description'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        
        self.repository.add(new_place)
        return new_place

    def get_place(self, place_id):
        """
        Retrieve a place by ID.
        
        Args:
            place_id: The ID of the place
        
        Returns:
            The Place object if found, None otherwise
        """
        return self.repository.get(place_id, 'Place')

    def get_all_places(self):
        """
        Retrieve all places.
        
        Returns:
            A list of all Place objects
        """
        return self.repository.get_all('Place')

    def update_place(self, place_id, place_data):
        """
        Update an existing place.
        
        Args:
            place_id: The ID of the place to update
            place_data: Dictionary with fields to update
        
        Returns:
            The updated Place object, or None if not found
        """
        place = self.repository.get(place_id, 'Place')
        if not place:
            return None
        
        place.update(place_data)
        self.repository.update(place)
        return place

    # ==================== REVIEW OPERATIONS ====================
    
    def create_review(self, review_data):
        """
        Create a new review.
        
        Args:
            review_data: Dictionary with review details, place_id, and user_id
        
        Returns:
            The newly created Review object
        """
        # Verify the place and user exist
        place = self.get_place(review_data['place_id'])
        user = self.get_user(review_data['user_id'])
        if not place or not user:
            return None
        
        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        
        self.repository.add(new_review)
        return new_review

    def get_review(self, review_id):
        """
        Retrieve a review by ID.
        
        Args:
            review_id: The ID of the review
        
        Returns:
            The Review object if found, None otherwise
        """
        return self.repository.get(review_id, 'Review')

    def get_all_reviews(self):
        """
        Retrieve all reviews.
        
        Returns:
            A list of all Review objects
        """
        return self.repository.get_all('Review')

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place.
        
        Args:
            place_id: The ID of the place
        
        Returns:
            A list of Review objects for that place
        """
        all_reviews = self.repository.get_all('Review')
        return [review for review in all_reviews if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        """
        Update an existing review.
        
        Args:
            review_id: The ID of the review to update
            review_data: Dictionary with fields to update
        
        Returns:
            The updated Review object, or None if not found
        """
        review = self.repository.get(review_id, 'Review')
        if not review:
            return None
        
        review.update(review_data)
        self.repository.update(review)
        return review

    def delete_review(self, review_id):
        """
        Delete a review.
        
        Args:
            review_id: The ID of the review to delete
        
        Returns:
            True if deleted successfully, False if not found
        """
        review = self.repository.get(review_id, 'Review')
        if not review:
            return False
        
        self.repository.delete(review_id, 'Review')
        return True

    # ==================== AMENITY OPERATIONS ====================
    
    def create_amenity(self, amenity_data):
        """
        Create a new amenity.
        
        Args:
            amenity_data: Dictionary with amenity name
        
        Returns:
            The newly created Amenity object
        """
        new_amenity = Amenity(name=amenity_data['name'])
        self.repository.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID.
        
        Args:
            amenity_id: The ID of the amenity
        
        Returns:
            The Amenity object if found, None otherwise
        """
        return self.repository.get(amenity_id, 'Amenity')

    def get_all_amenities(self):
        """
        Retrieve all amenities.
        
        Returns:
            A list of all Amenity objects
        """
        return self.repository.get_all('Amenity')

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity.
        
        Args:
            amenity_id: The ID of the amenity to update
            amenity_data: Dictionary with fields to update
        
        Returns:
            The updated Amenity object, or None if not found
        """
        amenity = self.repository.get(amenity_id, 'Amenity')
        if not amenity:
            return None
        
        amenity.update(amenity_data)
        self.repository.update(amenity)
        return amenity


# Create a single instance of the facade for the entire application
# This is called a Singleton pattern - ensures only one instance exists
facade = HBnBFacade()
