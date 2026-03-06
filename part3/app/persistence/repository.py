"""
Repository Pattern Implementation
The Repository acts as an in-memory data store.
It abstracts data access logic and provides a clean interface.
"""

class Repository:
    """
    In-memory repository for storing and retrieving model instances.
    
    The repository pattern provides a way to abstract data access logic.
    Benefits:
    - Easy to swap with a real database later
    - Business logic doesn't know about storage implementation
    - Centralized place to manage all data operations
    """
    
    def __init__(self):
        # Dictionary to store all objects: {entity_type: {id: object}}
        self.storage = {}

    def add(self, obj):
        """
        Add an object to the repository.
        
        Args:
            obj: The object to store (must have an 'id' attribute)
        """
        # Get the class name (e.g., 'User', 'Place')
        entity_type = obj.__class__.__name__
        
        # Initialize the entity type if it doesn't exist
        if entity_type not in self.storage:
            self.storage[entity_type] = {}
        
        # Store the object by its ID
        self.storage[entity_type][obj.id] = obj

    def get(self, obj_id, entity_type):
        """
        Retrieve an object by ID and entity type.
        
        Args:
            obj_id: The ID of the object to retrieve
            entity_type: The class name (e.g., 'User', 'Place')
        
        Returns:
            The object if found, None otherwise
        """
        if entity_type not in self.storage:
            return None
        return self.storage[entity_type].get(obj_id)

    def get_all(self, entity_type):
        """
        Retrieve all objects of a specific type.
        
        Args:
            entity_type: The class name (e.g., 'User', 'Place')
        
        Returns:
            A list of all objects of that type
        """
        if entity_type not in self.storage:
            return []
        return list(self.storage[entity_type].values())

    def update(self, obj):
        """
        Update an existing object.
        
        Args:
            obj: The object to update (must have an 'id' attribute)
        """
        entity_type = obj.__class__.__name__
        if entity_type in self.storage and obj.id in self.storage[entity_type]:
            self.storage[entity_type][obj.id] = obj

    def delete(self, obj_id, entity_type):
        """
        Delete an object by ID and entity type.
        
        Args:
            obj_id: The ID of the object to delete
            entity_type: The class name (e.g., 'User', 'Place')
        """
        if entity_type in self.storage and obj_id in self.storage[entity_type]:
            del self.storage[entity_type][obj_id]

    def find_by_attribute(self, entity_type, attribute, value):
        """
        Find an object by an attribute value (e.g., find user by email).
        
        Args:
            entity_type: The class name (e.g., 'User')
            attribute: The attribute name (e.g., 'email')
            value: The value to search for
        
        Returns:
            The first object matching the criteria, or None
        """
        if entity_type not in self.storage:
            return None
        
        for obj in self.storage[entity_type].values():
            if hasattr(obj, attribute) and getattr(obj, attribute) == value:
                return obj
        return None
