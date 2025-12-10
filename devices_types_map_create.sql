CREATE TABLE device_types_map (
    device_id INT REFERENCES devices(device_id) ON DELETE CASCADE,
    type_id INT REFERENCES device_types(type_id) ON DELETE RESTRICT,
    PRIMARY KEY (device_id, type_id)
);