CREATE TABLE device_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL, -- Например: "Вольтметр", "Термопара"
    measurement_unit VARCHAR(20)     -- Например: "В", "°C"
);