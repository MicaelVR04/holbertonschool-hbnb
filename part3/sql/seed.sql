PRAGMA foreign_keys = ON;

-- admin user (fixed ID)
INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '__ADMIN_BCRYPT_HASH__',
    1
);

-- amenities (UUID4)
INSERT INTO amenities (id, name) VALUES
('4b1f8d57-6cc9-4d66-8b86-d5d3ea6d9f59', 'WiFi'),
('97c1e8d1-e73f-4eb5-a238-0ce7d9a58f3b', 'Swimming Pool'),
('b8e3a17a-c8f8-4c9f-89ec-29e773844a0f', 'Air Conditioning');
