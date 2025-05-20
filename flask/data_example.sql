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