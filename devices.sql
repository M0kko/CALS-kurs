CREATE TABLE devices (
    device_id SERIAL PRIMARY KEY,
    serial_number VARCHAR(50) UNIQUE NOT NULL,
    inventory_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- Внешние ключи
    type_id INT REFERENCES device_types(type_id),
    location_id INT REFERENCES locations(location_id),
    responsible_id INT REFERENCES employees(employee_id),
    
    -- Экономические и временные показатели
    purchase_date DATE NOT NULL, -- Дата покупки (ввода в эксплуатацию)
    cost DECIMAL(10, 2) NOT NULL, -- Стоимость покупки
    service_life_months INT NOT NULL, -- Срок службы в месяцах
    
    -- Метрология
    last_verification_date DATE NOT NULL, -- Дата последней поверки
    verification_interval_months INT NOT NULL, -- Межповерочный интервал
    
    -- Статус и паспорт
    status VARCHAR(20) DEFAULT 'Active', -- Active, Storage, Written_Off
    passport_data JSONB -- Характеристики (диапазон, погрешность и т.д.)
);