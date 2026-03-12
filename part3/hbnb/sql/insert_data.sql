-- User admin initial
-- MDP : admin1234 (hashé avec bcrypt)
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$7WmsbEqjsU.8pyXreNUX9OIyuWPpKQ.aLZ3jePAP7OAVI48MymCP2',
    TRUE
);

-- Amenities
INSERT INTO Amenity (id, name) VALUES
    ('84e215b8-34ac-42ac-b7f1-9538622e17e7', 'WiFi'),
    ('5fb08c00-d262-4e9e-a047-a1669ac6aa46', 'Swimming Pool'),
    ('a0d743e7-1d5b-45c5-91f1-4711354ce6c7', 'Air Conditioning');