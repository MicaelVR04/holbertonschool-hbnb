# HBnB Evolution - Technical Documentation

## Task 1: High-Level Package Diagram

![HBnB High-Level Package Diagram](part1/HBnB_Project_Diagaram.png)

### 1. Layer Responsibilities

* **Presentation Layer (Services & API):**
    This is the entry point of the application. It handles all incoming client requests (via REST API endpoints) and returns the appropriate responses. Its primary job is to act as a translator between the user and the system's logic.
    * **Key Component:** Service API.

* **Business Logic Layer (Models):**
    The "brain" of the application. This layer enforces business rules and manages our core entities (User, Place, Review, and Amenity). It ensures data is valid before it is saved or updated.
    * **Key Components:** HBnB Facade, Domain Models.

* **Persistence Layer:**
    The "memory" of the application. It abstracts the storage logic so the rest of the system doesn't need to worry about *how* data is saved. In this stage, it manages data storage (initially file-based, transitioning to a database later).
    * **Key Component:** Database Access / Storage Engine.

---

### 2. The Facade Pattern

The **HBnB Facade** serves as a unified interface between the Presentation and Business Logic layers. 

**Why it is used:**
* **Simplification:** Instead of the API talking to every individual model (User, Place, etc.), it only communicates with the Facade.
* **Decoupling:** If we change how the models work internally, we only need to update the Facade. The API doesn't have to change at all.
* **Efficiency:** It coordinates complex operations (like creating a Place and linking it to an Owner) in one single call from the Presentation layer.
