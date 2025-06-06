-- 插入使用者基本資料
INSERT INTO users (username, plain_password, password, unit_name, farmer_name, phone, mobile, address, email, total_area, notes)
VALUES 
('farm_user01', 'password123', 'hashed_password123', 'Green Farm', 'John Doe', '123456789', '987654321', '123 Farm Road, City', 'john.doe@example.com', 10.5, '主要經營有機農業');

-- 插入農地資訊
INSERT INTO lands (user_id, number, lands_number, area, crop, notes)
VALUES 
(1, 'LAND001', '1234567890', 5.0, 'Tomatoes', '主要種植番茄'),
(1, 'LAND002', '0987654321', 3.0, 'Lettuce', '主要種植萵苣');

-- 插入生產計畫
INSERT INTO form002 (user_id, lands_id, area_code, area_size, month, crop_info, notes)
VALUES 
(1, 1, 'A01', 5.0, '2025-05', 'Tomatoes, Harvest in July, Estimated 500kg', '需注意病蟲害防治'),
(1, 2, 'B01', 3.0, '2025-05', 'Lettuce, Harvest in June, Estimated 300kg', '需注意灌溉管理');

-- 插入種子(苗)登記表
INSERT INTO form02 (user_id, lands_id, crop, crop_variety, seed_source, seedling_purchase_date, seedling_purchase_type, notes)
VALUES 
(1, 1, 'Tomatoes', 'Cherry Tomato', 'Local Supplier', '2025-03-01', 'Seed', '高品質種子'),
(1, 2, 'Lettuce', 'Romaine', 'Local Supplier', '2025-03-15', 'Seedling', '需注意溫度控制');

-- 插入栽培工作紀錄
INSERT INTO form03 (user_id, lands_id, operation_date, field_code, crop, crop_content, notes)
VALUES 
(1, 1, '2025-04-01', 'A01', 'Tomatoes', 'Soil preparation and fertilization', '使用有機肥料'),
(1, 2, '2025-04-05', 'B01', 'Lettuce', 'Planting seedlings', '需注意間距');

-- 插入肥料施用紀錄
INSERT INTO form06 (user_id, lands_id, date_used, field_code, crop, fertilizer_type, fertilizer_material_name, fertilizer_amount, dilution_factor, operator, process, notes)
VALUES 
(1, 1, '2025-04-10', 'A01', 'Tomatoes', 'Base Fertilizer', 'Organic Fertilizer A', 50.0, NULL, 'John Doe', 'Spread evenly on soil', '需注意均勻施用'),
(1, 2, '2025-04-12', 'B01', 'Lettuce', 'Top Dressing', 'Organic Fertilizer B', 30.0, NULL, 'John Doe', 'Apply near roots', '避免過量施用');

-- 插入肥料資材與代碼對照表
INSERT INTO form07 (user_id, fertilizer_material_code, fertilizer_material_name, manufacturer, supplier, packaging_unit, packaging_volume, notes)
VALUES 
(1, 'FERT001', 'Organic Fertilizer A', 'Green Fertilizer Co.', 'Local Supplier', 'Bag', '25kg', '適用於番茄'),
(1, 'FERT002', 'Organic Fertilizer B', 'Green Fertilizer Co.', 'Local Supplier', 'Bag', '20kg', '適用於萵苣');

-- 插入有害生物防治或環境消毒資材施用紀錄
INSERT INTO form09 (user_id, lands_id, date_used, field_code, crop, pest_target, pest_control_material_name, water_volume, chemical_usage, dilution_factor, safety_harvest_period, operator_method, operator, notes)
VALUES 
(1, 1, '2025-04-20', 'A01', 'Tomatoes', 'Aphids', 'Pesticide A', 100.0, 2.0, 50.0, 7, 'Spray evenly', 'John Doe', '需注意安全採收期'),
(1, 2, '2025-04-22', 'B01', 'Lettuce', 'Fungal Disease', 'Fungicide B', 80.0, 1.5, 40.0, 5, 'Spray evenly', 'John Doe', '避免過量使用');

-- 插入採收及採後處理紀錄
INSERT INTO form17 (user_id, lands_id, harvest_date, field_code, crop_name, batch_or_trace_no, harvest_weight, process_date, post_harvest_treatment, post_treatment_weight, verification_status, notes)
VALUES 
(1, 1, '2025-07-01', 'A01', 'Tomatoes', 'BATCH001', 500.0, '2025-07-02', 'Sorting and packing', 480.0, 'Verified', '品質良好'),
(1, 2, '2025-06-15', 'B01', 'Lettuce', 'BATCH002', 300.0, '2025-06-16', 'Washing and packing', 290.0, 'Verified', '需注意保鮮');

-- 插入客戶抱怨/回饋紀錄
INSERT INTO form22 (user_id, date, customer_name, customer_phone, complaint, resolution, processor_name, processor_date)
VALUES 
(1, '2025-07-10', 'Jane Smith', '123456789', 'Received damaged tomatoes', 'Provided replacement', 'John Doe', '2025-07-11');

-- 假設 user_id=1, lands_id=1 已存在

-- form10
INSERT INTO form10 (user_id, pest_control_material_code, pest_control_material_name, dosage_form, brand_name, supplier, packaging_unit, packaging_volume, notes)
VALUES (1, 'PCM001', '百滅寧', '水懸劑', '農友', '台灣農資', '瓶', '500ml', '常用殺菌劑');

-- form11
INSERT INTO form11 (user_id, pest_control_material_name, dosage_form, brand_name, supplier, packaging_unit, packaging_volume, date, purchase_quantity, usage_quantity, remaining_quantity, notes)
VALUES (1, '百滅寧', '水懸劑', '農友', '台灣農資', '瓶', '500ml', '2025-06-01', 10, 2, 8, '入庫');

-- form12
INSERT INTO form12 (user_id, lands_id, date_used, field_code, crop, other_material_name, usage_amount, operator, notes)
VALUES (1, 1, '2025-06-02', 'A1', '水稻', '石灰', 5, '王小明', '調整土壤酸鹼');

-- form13
INSERT INTO form13 (user_id, other_material_code, other_material_name, manufacturer, supplier, packaging_unit, packaging_volume, notes)
VALUES (1, 'OM001', '石灰', '台灣石灰', '台灣農資', '包', '20kg', '土壤改良');

-- form14
INSERT INTO form14 (user_id, other_material_name, manufacturer, supplier, packaging_unit, packaging_volume, date, purchase_quantity, usage_quantity, remaining_quantity, notes)
VALUES (1, '石灰', '台灣石灰', '台灣農資', '包', '20kg', '2025-06-01', 5, 1, 4, '入庫');

-- form15
INSERT INTO form15 (user_id, date, item, operation, recorder, notes)
VALUES (1, '2025-06-03', '倉庫', '清潔', '王小明', '每月例行');

-- form16
INSERT INTO form16 (user_id, date, item, operation, recorder, notes)
VALUES (1, '2025-06-03', '割草機', '保養', '王小明', '換機油');

-- form17
INSERT INTO form17 (user_id, lands_id, harvest_date, field_code, crop_name, batch_or_trace_no, harvest_weight, process_date, post_harvest_treatment, post_treatment_weight, verification_status, notes)
VALUES (1, 1, '2025-06-04', 'A1', '水稻', 'BATCH001', 1000, '2025-06-05', '乾燥', 950, '合格', '無');

-- form18
INSERT INTO form18 (user_id, arena, process_date, item, batch_number, fresh_weight, operation, dry_weight, remarks)
VALUES (1, '乾燥場', '2025-06-05', '水稻', 'BATCH001', 1000, '日曬', 950, '乾燥良好');

-- form19
INSERT INTO form19 (user_id, package, sale_date, product_name, sales_target, batch_number, shipment_quantity, packaging_spec, label_usage_quantity, label_void_quantity, verification_status)
VALUES (1, '包裝場', '2025-06-06', '白米', '超市', 'BATCH001', 900, '2kg/包', 450, 0, '合格');

-- form20
INSERT INTO form20 (user_id, checkitem, jobdate, operator_name)
VALUES (1, '健康檢查', '2025-06-05', '王小明');

-- form22
INSERT INTO form22 (user_id, date, customer_name, customer_phone, complaint, resolution, processor_name, processor_date)
VALUES (1, '2025-06-07', '李大華', '0912345678', '產品包裝破損', '補寄新品', '王小明', '2025-06-08');
-- 假設 user_id=1 已存在

INSERT INTO form08 (user_id, fertilizer_material_name, manufacturer, supplier, packaging_unit, packaging_volume, date, purchase_quantity, usage_quantity, remaining_quantity, notes)
VALUES 
(1, '尿素', '台肥', '台灣農資', '包', '20kg', '2025-06-01', 10, 2, 8, '基肥入庫'),
(1, '磷酸二銨', '台肥', '台灣農資', '包', '25kg', '2025-06-02', 5, 1, 4, '追肥入庫');