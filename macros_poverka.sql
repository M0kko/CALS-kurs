-- Показывает дату следующей поверки, считает типы через запятую
CREATE OR REPLACE VIEW view_verification_schedule AS
SELECT 
    d.device_id,
    d.inventory_number,
    -- Склеиваем типы: "Вольтметр, Амперметр"
    STRING_AGG(dt.type_name, ', ') as type_name, 
    d.device_name,
    d.last_verification_date,
    d.verification_interval_months,
    -- Расчет следующей даты
    (d.last_verification_date + (d.verification_interval_months || ' months')::interval)::date as next_verification_date,
    l.name as location,
    e.last_name || ' ' || LEFT(e.first_name, 1) || '.' as responsible_person
FROM devices d
LEFT JOIN device_types_map map ON d.device_id = map.device_id
LEFT JOIN device_types dt ON map.type_id = dt.type_id
JOIN locations l ON d.location_id = l.location_id
JOIN employees e ON d.responsible_id = e.employee_id
GROUP BY d.device_id, l.name, e.last_name, e.first_name;