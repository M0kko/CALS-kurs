CREATE TABLE device_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL,
    measurement_unit VARCHAR(20)
);