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
from app.persistence.repository import Repository, SQLAlchemyRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.repository = Repository()               # temporary for non-user entities
        self.user_repo = SQLAlchemyRepository(User) # users now via SQLAlchemy

    # ==================== USER OPERATIONS ====================

    def create_user(self, user_data):
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=bool(user_data.get('is_admin', False))
        )
        new_user.hash_password(user_data['password'])
        self.user_repo.add(new_user)
        return new_user

    def get_user_by_email(self, email):
        return self.user_repo.find_by_attribute('email', email)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    # ==================== PLACE OPERATIONS ====================

    def create_place(self, place_data):
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
        return self.repository.get(place_id, 'Place')

    def get_all_places(self):
        return self.repository.get_all('Place')

    def update_place(self, place_id, place_data):
        place = self.repository.get(place_id, 'Place')
        if not place:
            return None

        place.update(place_data)
        self.repository.update(place)
        return place

    # ==================== REVIEW OPERATIONS ====================

    def create_review(self, review_data):
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
        return self.repository.get(review_id, 'Review')

    def get_all_reviews(self):
        return self.repository.get_all('Review')

    def get_reviews_by_place(self, place_id):
        all_reviews = self.repository.get_all('Review')
        return [review for review in all_reviews if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.repository.get(review_id, 'Review')
        if not review:
            return None

        review.update(review_data)
        self.repository.update(review)
        return review

    def delete_review(self, review_id):
        review = self.repository.get(review_id, 'Review')
        if not review:
            return False

        self.repository.delete(review_id, 'Review')
        return True

    # ==================== AMENITY OPERATIONS ====================

    def create_amenity(self, amenity_data):
        new_amenity = Amenity(name=amenity_data['name'])
        self.repository.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        return self.repository.get(amenity_id, 'Amenity')

    def get_all_amenities(self):
        return self.repository.get_all('Amenity')

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.repository.get(amenity_id, 'Amenity')
        if not amenity:
            return None

        amenity.update(amenity_data)
        self.repository.update(amenity)
        return amenity


facade = HBnBFacade()
