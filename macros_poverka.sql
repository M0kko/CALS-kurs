-- Макрос 2: План поверки (Кто просрочен или должен поверяться в текущем месяце)
CREATE OR REPLACE VIEW view_verification_schedule AS
SELECT 
    d.device_id,
    d.inventory_number,
    dt.type_name,
    d.last_verification_date,
    d.verification_interval_months,
    -- Расчет даты следующей поверки
    (d.last_verification_date + (d.verification_interval_months || ' months')::interval)::date as next_verification_date,
    l.name as location,
    e.last_name || ' ' || LEFT(e.first_name, 1) || '.' as responsible_person
FROM devices d
JOIN device_types dt ON d.type_id = dt.type_id
JOIN locations l ON d.location_id = l.location_id
JOIN employees e ON d.responsible_id = e.employee_id;