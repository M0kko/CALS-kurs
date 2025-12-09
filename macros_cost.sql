-- Макрос 1: Расчет амортизации и остаточной стоимости
-- Формула: Стоимость - (Стоимость * (Прожитые месяцы / Срок службы))
CREATE OR REPLACE VIEW view_depreciation AS
SELECT 
    d.inventory_number,
    dt.type_name,
    d.purchase_date,
    d.cost as initial_cost,
    d.service_life_months,
    -- Расчет возраста в месяцах (приблизительно)
    ROUND((EXTRACT(EPOCH FROM (NOW() - d.purchase_date)) / 2592000)::numeric, 1) as months_used,
    -- Остаточная стоимость (если < 0, то 0)
    GREATEST(0, ROUND(
        (d.cost - (d.cost * (EXTRACT(EPOCH FROM (NOW() - d.purchase_date)) / 2592000) / NULLIF(d.service_life_months, 0)))::numeric, 
    2)) as current_value
FROM devices d
JOIN device_types dt ON d.type_id = dt.type_id;
