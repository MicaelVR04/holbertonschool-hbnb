"""In-memory repository for storing entities."""

class Repository:
    """In-memory repository for managing entities with basic CRUD operations."""
    
    def __init__(self):
        """Initialize the repository with empty storage."""
        self._storage = {}
    
    def add(self, entity):
        """
        Add an entity to the repository.
        
        Args:
            entity: The entity to add (must have an 'id' attribute)
        """
        self._storage[entity.id] = entity
    
    def get(self, entity_id):
        """
        Retrieve an entity by ID.
        
        Args:
            entity_id: The ID of the entity to retrieve
            
        Returns:
            The entity if found, None otherwise
        """
        return self._storage.get(entity_id)
    
    def get_all(self):
        """
        Retrieve all entities.
        
        Returns:
            A list of all entities
        """
        return list(self._storage.values())
    
    def update(self, entity_id, data):
        """
        Update an entity by ID.
        
        Args:
            entity_id: The ID of the entity to update
            data: Dictionary containing the attributes to update
            
        Returns:
            The updated entity if found, None otherwise
        """
        entity = self._storage.get(entity_id)
        if entity:
            entity.update(data)
            return entity
        return None
    
    def delete(self, entity_id):
        """
        Delete an entity by ID.
        
        Args:
            entity_id: The ID of the entity to delete
            
        Returns:
            True if deleted, False if not found
        """
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
