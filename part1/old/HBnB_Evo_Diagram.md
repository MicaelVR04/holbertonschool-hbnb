# HBnB Evolution: API Sequence Diagrams

This document outlines the interaction flow between the Presentation, Business Logic, and Persistence layers for four key API calls within the HBnB application.

## 1. User Registration
**Purpose**: To securely register a new user into the system.
* **Process**: The `ServiceAPI` (Presentation) receives the POST request. The `HBnB_Facade` (Business Logic) validates the input and hashes the user's password. Finally, the `Database` (Persistence) commits the new user record.

![User Registration](./HBnB_User_Reg.png)

---

## 2. Place Creation
**Purpose**: To allow an authorized user to list a new property.
* **Process**: The API layer receives the property details. The Logic layer verifies that the owner exists and that the property data (price, location) meets business rules. The storage layer then creates the entry.

![Place Creation](./HBnB_Place_Creation.png)

---

## 3. Review Submission
**Purpose**: To record user feedback and ratings for a specific place.
* **Process**: The `AppGateway` captures the review. The `BusinessLogicHandler` checks if the rating is between 1 and 5 and ensures the user is linked to the correct place before the `DataRepository` saves it.

![Review Submission](./HBnB_Review_Sub.png)

---

## 4. Fetching a List of Places
**Purpose**: To retrieve property listings based on user-defined filters.
* **Process**: The `PlaceController` receives a GET request with optional filters. The `ListingManager` processes these criteria and queries the `PersistenceStore` to return the relevant data array.

![List Places](./HBnB_Fetching.png)
