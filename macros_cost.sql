-- Считает остаточную стоимость линейным методом по месяцам
CREATE OR REPLACE VIEW view_depreciation AS
SELECT 
    d.inventory_number,
    STRING_AGG(dt.type_name, ', ') as type_name,
    d.device_name,
    d.purchase_date,
    d.cost as initial_cost,
    d.service_life_months,
    -- Сколько месяцев используется
    ROUND((EXTRACT(EPOCH FROM (NOW() - d.purchase_date)) / 2592000)::numeric, 1) as months_used,
    -- Формула остаточной стоимости: Цена - (Цена * (ПрошлоМес / ВсегоМес))
    GREATEST(0, ROUND(
        (d.cost - (d.cost * (EXTRACT(EPOCH FROM (NOW() - d.purchase_date)) / 2592000) / NULLIF(d.service_life_months, 0)))::numeric, 
    2)) as current_value
FROM devices d
LEFT JOIN device_types_map map ON d.device_id = map.device_id
LEFT JOIN device_types dt ON map.type_id = dt.type_id
GROUP BY d.device_id;