# HBnB Evolution: Business Logic Class Diagram

![HBnB Class Diagram](./Detailed_Class.png)

## Entity Descriptions

* **BaseModel**: The parent class for all entities in the system. It provides a unique identifier (UUID4) and audit timestamps (`created_at`, `updated_at`) for every object. Methods include `save()` to update timestamps and `to_dict()` for serialization.
* **User**: Represents individuals in the system. Key attributes include `email`, `password`, `first_name`, `last_name`, and `is_admin` status.
* **Place**: Represents properties listed for rental. Key attributes include `title`, `description`, `price`, `latitude`, and `longitude`.
* **Review**: Represents feedback left by users for specific places. Key attributes include the `text` of the review and a `rating` (1-5).
* **Amenity**: Represents features available at a place (e.g., WiFi, AC). Key attributes include `name` and `description`.

---

## Relationships and Logic

* **Inheritance**: User, Place, Review, and Amenity all inherit from **BaseModel**. This ensures global consistency for unique identifiers and creation tracking across the Business Logic layer.
* **Association (User to Place)**: 1:N relationship. A User (Owner) can list zero or many Places. Each Place is associated with exactly one User.
* **Association (User to Review)**: 1:N relationship. A User can author multiple reviews. Each review belongs to one author.
* **Association (Place to Review)**: 1:N relationship. A Place can receive multiple reviews. This structure allows the system to aggregate user feedback for a specific property.
* **Association (Place to Amenity)**: N:N relationship. A Place can have multiple amenities, and an Amenity can be linked to multiple Places.

---

## Implementation Details

* **Identifiers**: All entities use UUID4 for unique identification to prevent collision.
* **Lifecycle**: The `created_at` and `updated_at` attributes in the BaseModel handle the lifecycle tracking for every entity instance.
