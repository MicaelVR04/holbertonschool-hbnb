# HBnB - Part 2: Business Logic & API Implementation

A REST API built with Flask and Flask-RESTx implementing the core business logic for an Airbnb-like application.

## Project Overview

This project implements a three-layer architecture separating concerns:
- **Presentation Layer**: RESTful API endpoints with automatic documentation
- **Business Logic Layer**: Facade pattern for centralized business operations
- **Persistence Layer**: Repository pattern for data access abstraction

## Project Structure

```
app/
├── api/
│   └── v1/
│       ├── users.py
│       ├── places.py
│       ├── reviews.py
│       └── amenities.py
├── models/
│   ├── base_model.py
│   ├── user.py
│   ├── place.py
│   ├── review.py
│   └── amenity.py
├── services/
│   └── facade.py
└── persistence/
    └── repository.py
```

## Core Entities

- **User**: Platform users with email validation
- **Place**: Properties with validation for price and coordinates
- **Review**: Ratings and feedback on places
- **Amenity**: Services/features available at places

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
python3 run.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### Users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/<id>` - Get user by ID
- `PUT /api/v1/users/<id>` - Update user

### Places
- `POST /api/v1/places/` - Create place
- `GET /api/v1/places/` - List all places
- `GET /api/v1/places/<id>` - Get place by ID
- `PUT /api/v1/places/<id>` - Update place

### Reviews
- `POST /api/v1/reviews/` - Create review
- `GET /api/v1/reviews/` - List all reviews
- `GET /api/v1/reviews/<id>` - Get review by ID
- `PUT /api/v1/reviews/<id>` - Update review
- `DELETE /api/v1/reviews/<id>` - Delete review
- `GET /api/v1/reviews/places/<place_id>` - Get reviews for a place

### Amenities
- `POST /api/v1/amenities/` - Create amenity
- `GET /api/v1/amenities/` - List all amenities
- `GET /api/v1/amenities/<id>` - Get amenity by ID
- `PUT /api/v1/amenities/<id>` - Update amenity

## Testing

### Using cURL

```bash
# Create a user
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com"}'

# Get all places
curl -X GET http://localhost:5000/api/v1/places/

# Create a review
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text":"Great place!","rating":5,"place_id":"<place_id>","user_id":"<user_id>"}'
```

### Using Swagger

Automatic API documentation is available at `http://localhost:5000` via Flask-RESTx

## Error Handling

All validation errors return `400 Bad Request` with descriptive messages:
- Invalid email format
- Empty required fields
- Out-of-range values (e.g., latitude, rating)
- Duplicate constraints

## Architecture Highlights

- **UUID**: Non-enumerable IDs for all entities
- **Timestamps**: Automatic creation and modification timestamps
- **Validation**: Multi-layer validation at model and API levels
- **Relationships**: Proper entity relationships (User-Place, Place-Review, etc.)

