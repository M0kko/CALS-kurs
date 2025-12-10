-- Термометр
INSERT INTO device_types_map (device_id, type_id) VALUES (1, 1);
-- Датчик давления
INSERT INTO device_types_map (device_id, type_id) VALUES (2, 2);
-- Мультиметр (ID 3) является и Вольтметром (ID 4), и Амперметром (ID 5)
INSERT INTO device_types_map (device_id, type_id) VALUES (3, 4), (3, 5); 
-- Расходомер
INSERT INTO device_types_map (device_id, type_id) VALUES (4, 3);
-- pH-метр
INSERT INTO device_types_map (device_id, type_id) VALUES (5, 6);
-- Весы
INSERT INTO device_types_map (device_id, type_id) VALUES (6, 9);
-- Гигрометр
INSERT INTO device_types_map (device_id, type_id) VALUES (7, 10);
-- Уровнемер
INSERT INTO device_types_map (device_id, type_id) VALUES (8, 7);
-- Кондуктометр
INSERT INTO device_types_map (device_id, type_id) VALUES (9, 8);
-- Амперметр
INSERT INTO device_types_map (device_id, type_id) VALUES (10, 5);