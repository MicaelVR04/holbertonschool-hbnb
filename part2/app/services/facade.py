"""Facade pattern implementation for business logic layer."""

from app.persistence.repository import Repository
from app.models.user import User

class HBnBFacade:
    """Facade that provides the interface for the API layer to interact with business logic."""
    
    def __init__(self):
        """Initialize the facade with repository instances."""
        self.user_repository = Repository()
    
    # User-related methods
    def create_user(self, user_data):
        """
        Create a new user.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            The created User object
        """
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email')
        )
        self.user_repository.add(user)
        return user
    
    def get_user(self, user_id):
        """
        Retrieve a user by ID.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            The User object if found, None otherwise
        """
        return self.user_repository.get(user_id)
    
    def get_all_users(self):
        """
        Retrieve all users.
        
        Returns:
            A list of all User objects
        """
        return self.user_repository.get_all()
    
    def get_user_by_email(self, email):
        """
        Retrieve a user by email.
        
        Args:
            email: The email address of the user
            
        Returns:
            The User object if found, None otherwise
        """
        users = self.user_repository.get_all()
        for user in users:
            if user.email == email:
                return user
        return None
    
    def update_user(self, user_id, user_data):
        """
        Update a user's information.
        
        Args:
            user_id: The ID of the user to update
            user_data: Dictionary containing the fields to update
            
        Returns:
            The updated User object if found, None otherwise
        """
        return self.user_repository.update(user_id, user_data)


# Create a single instance of the facade to be used throughout the application
facade = HBnBFacade()
