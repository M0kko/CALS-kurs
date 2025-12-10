CREATE TABLE devices (
    device_id SERIAL PRIMARY KEY,
    serial_number VARCHAR(50) UNIQUE NOT NULL,
    inventory_number VARCHAR(50) UNIQUE NOT NULL,
    device_name VARCHAR(100) NOT NULL, -- Название модели (напр. "FLUKE-87")
    
    -- Внешние ключи
    location_id INT REFERENCES locations(location_id),
    responsible_id INT REFERENCES employees(employee_id),
    
    -- Экономика и ЖЦ
    purchase_date DATE NOT NULL,
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    service_life_months INT NOT NULL DEFAULT 120, -- Срок службы (10 лет по умолч.)
    
    -- Метрология
    last_verification_date DATE NOT NULL,
    verification_interval_months INT NOT NULL DEFAULT 12,
    
    -- Прочее
    status VARCHAR(20) DEFAULT 'В эксплуатации' CHECK (status IN ('В эксплуатации', 'На складе', 'Списан', 'В ремонте')),
    passport_data JSONB -- Технические характеристики (диапазон, погрешность)
);