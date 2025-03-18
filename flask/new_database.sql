CREATE DATABASE IF NOT EXISTS new_database;
USE new_database;

-- users（使用者基本資料）
CREATE TABLE users(
    ID          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50) NOT NULL UNIQUE COMMENT '帳號',
    plain_password  VARCHAR(255) COMMENT '原始密碼',
    password    VARCHAR(255) NOT NULL COMMENT '加密後的密碼',
    unit_name   VARCHAR(50) COMMENT '單位名稱',
    farmer_name VARCHAR(50) COMMENT '經營農戶姓名',
    phone       VARCHAR(50) COMMENT '聯絡電話',
    fax         VARCHAR(50) COMMENT '傳真',
    mobile      VARCHAR(50) COMMENT '行動電話',
    address     VARCHAR(50) COMMENT '住址',
    email       VARCHAR(50) COMMENT 'e-mail',
    total_area  DECIMAL(10,2) COMMENT '栽培總面積',
    notes       VARCHAR(50) COMMENT '備註',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入使用者資料
INSERT INTO users (username, plain_password, password, unit_name, farmer_name, phone, fax, mobile, address, email, total_area, notes)
VALUES
    ('帳號', '原始密碼', '加密後的密碼', '單位名稱', '經營農戶姓名', '聯絡電話', '傳真', '行動電話', '住址', 'e-mail', 5.5, '備註'),
    ('farmer1', '原始密碼', 'hashed_password', '農場 A', '張三', '02-12345678', '02-87654321', '0912-345678', '住址', 'farmer1@example.com', 5.5, 'notes'),
    ('farmer2', '原始密碼', 'hashed_password', '農場 B', '張三', '02-12345678', '02-87654321', '0912-345678', '台北市XX路', 'farmer1@example.com', 5.5, 'notes'),
    ('newuser', 'password123', '加密後的密碼', 'New User Unit', 'New User', '987654321', '987654321', '987654321', 'New User Address', 'newuser@example.com', 0, 'New user notes'),
    ('user', '123456', '加密後的密碼', 'User Unit', 'User', '123456789', '123456789', '123456789', 'User Address', 'user@example.com', 0, 'User notes');

-- 更新資料庫中的密碼哈希
UPDATE users SET password = 'scrypt:32768:8:1$GecnsTV9ESdKmZ6l$87571fe224e1a108335d3061c51aca78e66d1a4d7f3a42cf3bcbdee24a6cb38bb08f3c36d411cbb4b0a173639f5ef7b77d3e1810497db66c43586e52c40afc85' WHERE username = 'newuser';
UPDATE users SET password = 'scrypt:32768:8:1$GecnsTV9ESdKmZ6l$87571fe224e1a108335d3061c51aca78e66d1a4d7f3a42cf3bcbdee24a6cb38bb08f3c36d411cbb4b0a173639f5ef7b77d3e1810497db66c43586e52c40afc85' WHERE username = 'user';

-- lands（農地資訊）
CREATE TABLE lands (
    id                 INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id            INT NOT NULL,                    -- 關聯 `users` 表
    -- lands 表中的 user_id 是手動指定的，並且必須是 users 表中已經存在的 id
    number             VARCHAR(50),            -- 農地編號
    lands_number       VARCHAR(50),            -- 農地地籍號碼
    area               DECIMAL(10,2),          -- 面積（單位：公頃）
    crop               VARCHAR(100),                    -- 種植作物
    notes              TEXT,                            -- 備註
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
-- 資料示例lands（農地資訊）
INSERT INTO lands (user_id, number, lands_number, area, crop, notes)
VALUES
    (1, '農地編號', '農地地籍號碼', 1.2, '種植作物', '備註'),
    (2, 'LP001', '123456-7890', 1.2, '小白菜', '土壤肥沃，適合蔬菜種植'),
    (1, 'LP002', '123456-7891', 2.5, '玉米', '土壤較乾燥，適合玉米種植');

-- 查詢農戶的所有農地
SELECT u.username, u.farmer_name, l.lands_number, l.area, l.crop, l.notes
FROM users u
JOIN lands l ON u.id = l.user_id
WHERE u.username = 'farmer1';

-- form002（生產計畫）
CREATE TABLE form002 (
    id               INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id          INT NOT NULL,                    -- 關聯 `users` 表
    lands_id         INT NOT NULL,                    -- 關聯 `lands` 表
    area_code        VARCHAR(20),                     -- 場區代號
    area_size        DECIMAL(10,2),                   -- 場區面積（公頃）
    month            VARCHAR(10),                     -- 月份（1月-12月）
    crop_info        VARCHAR(255),                    -- 種植作物種類、產期、預估產量（公斤）
    notes            TEXT,                             -- 備註
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lands_id) REFERENCES lands(id) ON DELETE CASCADE
);
-- 資料示例form002（生產計畫）
INSERT INTO form002 (user_id,lands_id, area_code, area_size, month, crop_info, notes)
VALUES 
    (1,1,  '場區代號', 2.5, '月份', '種植作物種類、產期、預估產量（公斤）', '備註'),
    (1,2,  'AC123456', 2.5, '3月', '小白菜/1000', '間作及敷蓋稻草'),
    (1,3,  'AC654321', 1.8, '6月', '玉米/500', '施有機肥'),
    (2,3,  'AC987654', 3.2, '9月', '水稻/2000', '水源充足');

-- 確保 form002 表中的 area_code 欄位只能選擇 lands 表中的 number 欄位值。

SELECT u.username, u.farmer_name, f.area_code, f.area_size, f.month, f.crop_info, f.notes
FROM form002 f
JOIN users u ON f.user_id = u.id
JOIN lands l ON f.lands_id = l.id
WHERE u.username = 'farmer1';

-- form02（種子(苗)登記表）
CREATE TABLE form02 (
    id                   INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id              INT NOT NULL,                    -- 關聯 `users` 表
    cultivated_crop      VARCHAR(100),           -- 栽培作物
    crop_variety         VARCHAR(100),           -- 栽培品種
    seed_source          VARCHAR(255),           -- 種子(苗)來源
    seedling_purchase_date DATE NULL,                -- 育苗(購入)日期
    seedling_purchase_type VARCHAR(50),         -- 育苗(購入)種類
    notes                TEXT,                            -- 備註
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 資料示例form02（種子(苗)登記表）
INSERT INTO form02 (user_id, cultivated_crop, crop_variety, seed_source, seedling_purchase_date, seedling_purchase_type, notes)
VALUES 
    (1,  '高麗菜', '高麗菜', '自行育苗', '2025-02-01', '種苗', '間作及敷蓋稻草'),
    (2, '高麗菜', '高麗菜', '自行育苗', '2025-02-01', '種苗', '間作及敷蓋稻草'),
    (2, '高麗菜', '高麗菜', '購買來源：XYZ公司', '2025-03-15', '種子', '施有機肥'),
    (1,  '高麗菜', '高麗菜', '購買來源：XYZ公司', '2025-03-15', '種子', '施有機肥');

-- 查詢某農戶的所有種子登記
SELECT u.username, u.farmer_name, f.cultivated_crop, f.crop_variety, f.seed_source, f.seedling_purchase_date, f.seedling_purchase_type, f.notes
FROM form02 f
JOIN users u ON f.user_id = u.id
WHERE u.username = 'farmer1';

-- form03（栽培工作紀錄）
CREATE TABLE form03 (
    id                   INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id              INT NOT NULL,                    -- 關聯 `users` 表

    operation_date       DATE NULL,                   -- 作業日期
    field_code           VARCHAR(50),            -- 田區代號
    crop                 VARCHAR(100),           -- 作物
    crop_content         TEXT,                   -- 作物內容（工作代碼及描述）
    notes                TEXT,                            -- 備註
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    -- FOREIGN KEY (lands_id) REFERENCES lands(id) ON DELETE CASCADE
);

-- 資料示例form03（栽培工作紀錄）
INSERT INTO form03 (user_id, operation_date, field_code, crop, crop_content, notes)
VALUES 
    (1, '2025-02-01', 'F000-0000', '高麗菜', '1-1 整地, 4-2 灌溉', '間作及敷蓋稻草'),
    (1, '2025-02-05', 'F000-0001', '高麗菜', '2-1 介質消毒, 5-2 追肥', '使用有機肥料'),
    (2, '2025-03-15', 'F000-0002', '小黃瓜', '4-3 培土, 6-6 除草', '增加水源');

-- 查詢某農戶的所有栽培工作紀錄
SELECT u.username, u.farmer_name, f.operation_date, f.field_code, f.crop, f.crop_content, f.notes
FROM form03 f
JOIN users u ON f.user_id = u.id

WHERE u.username = 'farmer1';

-- form06（肥料施用紀錄）
CREATE TABLE form06 (
    id                 INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id            INT NOT NULL,           -- 關聯 `users` 表
    date_used          DATE NULL,           -- 使用日期
    field_code         VARCHAR(20),           -- 田區代號
    crop               VARCHAR(50),           -- 作物
    fertilizer_type    VARCHAR(100),           -- 施肥別 (基肥, 追肥)
    material_code_or_name VARCHAR(100),       -- 資材代碼或資材名稱
    fertilizer_amount  DECIMAL(10, 2),           -- 肥料使用量 (公斤/公升)
    dilution_factor    DECIMAL(5, 2),           -- 稀釋倍數 (液肥適用)
    operator           VARCHAR(100),           -- 操作人員
    process            TEXT,                            -- 製作流程
    notes              TEXT,                            -- 備註
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
-- 資料示例form06（肥料施用紀錄）
INSERT INTO form06 (user_id, date_used, field_code, crop, fertilizer_type, material_code_or_name, fertilizer_amount, dilution_factor, operator, process, notes)
VALUES 
    (1, '2025-02-01', 'F000-0000', '高麗菜', '基肥', 'M000-0000', 10.00, NULL, '王小明', '間作及敷蓋稻草', '注意施肥均勻'),
    (1, '2025-03-15', 'F000-0001', '小白菜', '追肥', 'ooxx資材', 15.00, 0.5, '李小華', '進行追肥', '施肥後進行灌溉');
-- 查詢某田區的所有肥料施用紀錄
SELECT f.date_used, f.field_code, f.crop, f.fertilizer_type, f.material_code_or_name, f.fertilizer_amount, f.dilution_factor, f.operator, f.process, f.notes
FROM form06 f
JOIN users u ON f.user_id = u.id
WHERE f.field_code = 'F000-0000';

-- form07（肥料資材與代碼對照表）
CREATE TABLE form07 (
    id INT AUTO_INCREMENT PRIMARY KEY,                    -- 唯一編號
    user_id INT NOT NULL,                                  -- 關聯 `users` 表
    fertilizer_material_code VARCHAR(20),          -- 肥料資材代碼
    fertilizer_material_name VARCHAR(100),         -- 肥料資材名稱
    notes TEXT,                                            -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,         -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, -- 外鍵，關聯 `users` 表
    UNIQUE(fertilizer_material_code)                        -- 确保 `fertilizer_material_code` 是唯一的
);

-- 插入資料範例
INSERT INTO form07 (user_id, fertilizer_material_code, fertilizer_material_name, notes)
VALUES (1, 'M000-0000', 'ooxx資材', '備註'),
       (1, 'M000-0001', 'yyzz資材', '適合高濃度施用');

-- 查詢與 `users` 表關聯的肥料資材代碼及名稱
SELECT f.fertilizer_material_code, f.fertilizer_material_name, f.notes, u.username, u.farmer_name
FROM form07 f
JOIN users u ON f.user_id = u.id
WHERE f.fertilizer_material_code = 'M000-0000';



-- form08（肥料入出庫紀錄）
CREATE TABLE form08 (
    id INT AUTO_INCREMENT PRIMARY KEY,                     -- 編號，自動遞增
    user_id              INT NOT NULL,                    -- 關聯 `users` 表
    material_name VARCHAR(100),                    -- 資材名稱
    manufacturer VARCHAR(100),                              -- 廠商
    supplier VARCHAR(100),                                  -- 供應商
    packaging_unit VARCHAR(100), -- 包裝單位□包 □瓶 □罐 □其他_______
    packaging_volume VARCHAR(50),                  -- 包裝容量，前面是數字，後面試單位選項（如：公克、公斤、毫升、公升等）
    date DATE NULL,                                     -- 日期
    purchase_quantity DECIMAL(10, 2),              -- 購入量
    usage_quantity DECIMAL(10, 2),                 -- 使用量
    remaining_quantity DECIMAL(10, 2),            -- 剩餘量
    notes TEXT,                                             -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,         -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- 外鍵，關聯 `users` 表
);
--  資料示例form08（肥料入出庫紀錄）
INSERT INTO form08 (user_id, material_name, manufacturer, supplier, packaging_unit, packaging_volume, date, purchase_quantity, usage_quantity, remaining_quantity, notes)
VALUES 
    (1, 'ooxx資材', '某某廠商', '某某供應商', '包', '10公斤', '2025-02-05', 100.00, 10.00, 90.00, '無');
-- 查詢肥料入出庫紀錄
SELECT f.id, f.material_name, f.manufacturer, f.supplier, f.packaging_unit, f.packaging_volume, 
       f.date, f.purchase_quantity, f.usage_quantity, f.remaining_quantity, f.notes, 
       u.username, u.farmer_name
FROM form08 f
JOIN users u ON f.user_id = u.id
WHERE f.material_name = 'ooxx資材';

-- form09（有害生物防治或環境消毒資材施用紀錄）
CREATE TABLE form09 (
    id INT AUTO_INCREMENT PRIMARY KEY,                        -- 編號，自動遞增
    user_id INT NOT NULL,                    -- 關聯 `users` 表
    date_used DATE NULL,                                   -- 使用日期
    field_code VARCHAR(50),                            -- 田區代號
    crop VARCHAR(100),                                -- 作物名稱
    pest_target VARCHAR(100),                         -- 防治對象（如：蟲）
    material_code_or_name VARCHAR(100),               -- 資材代碼或名稱
    water_volume DECIMAL(10, 2),                      -- 用水量（公升）
    chemical_usage DECIMAL(10, 2),                    -- 藥劑使用量（公斤、公升）
    dilution_factor DECIMAL(10, 2),                   -- 稀釋倍數
    safety_harvest_period INT,                        -- 安全採收期（天）
    operator_method VARCHAR(100),  -- 操作方式
    operator VARCHAR(100),                            -- 操作人員
    notes TEXT,                                                -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,            -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- 外鍵，關聯 `users` 表
);
-- 資料示例 form09（有害生物防治或環境消毒資材施用紀錄）
INSERT INTO form09 (user_id, date_used, field_code, crop, pest_target, material_code_or_name, water_volume, chemical_usage, dilution_factor, safety_harvest_period, operator_method, operator, notes)
VALUES 
    (1, '2025-02-05', 'F000-0000', '高麗菜', '蟲', 'M000-0000', 10.00, 0.5, 2.4, 14, '噴灑', '王小明', '無');
-- 查詢有害生物防治或環境消毒資材施用紀錄
SELECT id, date_used, field_code, crop, pest_target, material_code_or_name, water_volume, chemical_usage, dilution_factor, safety_harvest_period, operator_method, operator, notes
FROM form09
WHERE crop = '高麗菜' AND pest_target = '蟲';

-- form10（防治資材與代碼對照表）
CREATE TABLE form10 (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id INT NOT NULL,               -- 關聯 `users` 表
    pest_control_material_code VARCHAR(100),   -- 防治資材代碼
    pest_control_material_name VARCHAR(100),   -- 防治資材名稱
    notes TEXT,                                              -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,          -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 插入資料範例
INSERT INTO form10 (user_id, pest_control_material_code, pest_control_material_name, notes)
VALUES (1, 'M000-0000', 'ooxx資材', '用於防治蟲害，間作及敷蓋稻草');

-- 查詢防治資材代碼及名稱
SELECT u.username, u.farmer_name, f.pest_control_material_code, f.pest_control_material_name, f.notes
FROM form10 f
JOIN users u ON f.user_id = u.id
WHERE f.pest_control_material_code = 'M000-0000';


-- form11（有害生物防治或環境消毒資材入出庫紀錄）
CREATE TABLE form11 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                             -- 關聯 `users` 表
    material_name VARCHAR(255),              -- 資材名稱
    dosage_form VARCHAR(100),                        -- 劑型
    brand_name VARCHAR(100),                         -- 商品名(廠牌)
    supplier VARCHAR(100),                           -- 供應商
    packaging_unit VARCHAR(100),             -- 包裝單位
    packaging_volume VARCHAR(100),                  -- 包裝容量
    date DATE NULL,                              -- 日期
    purchase_quantity DECIMAL(10, 2),                -- 購入量
    usage_quantity DECIMAL(10, 2),                   -- 使用量
    remaining_quantity DECIMAL(10, 2),               -- 剩餘量
    notes TEXT,                                              -- 備註

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE  -- 外鍵，關聯 `users` 表
);
-- 資料示例form11（有害生物防治或環境消毒資材入出庫紀錄）
INSERT INTO form11 (user_id, material_name, dosage_form, brand_name, supplier, packaging_unit, packaging_volume, date, purchase_quantity, usage_quantity, remaining_quantity, notes)
VALUES 
    (1, 'ooxx資材', '顆粒型', '某某廠', '供應商A', '包', 10.0, '2025-02-05', 20.0, 10.0, 10.0, '無');
-- 查詢有害生物防治或環境消毒資材入出庫紀錄
SELECT f.id, f.material_name, f.dosage_form, f.brand_name, f.supplier, f.packaging_unit, 
       f.packaging_volume, f.date, f.purchase_quantity, f.usage_quantity, f.remaining_quantity, 
       u.username, u.farmer_name, f.notes
FROM form11 f
JOIN users u ON f.user_id = u.id
WHERE f.material_name = 'ooxx資材';

-- form12（其他資材使用紀錄）
CREATE TABLE form12 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                             -- 關聯 `users` 表
    date_used DATE NULL,                          -- 使用日期
    field_code VARCHAR(100),                 -- 田區代號
    crop VARCHAR(100),                       -- 作物名稱
    material_code_or_name VARCHAR(255),      -- 資材代碼或資材名稱
    usage_amount DECIMAL(10, 2),             -- 使用量
    operator VARCHAR(100),                   -- 操作人員
    notes TEXT,                                       -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE  -- 外鍵，關聯 `users` 表
);

-- 資料示例form12（其他資材使用紀錄）
INSERT INTO form12 (user_id, date_used, field_code, crop, material_code_or_name, usage_amount, operator, notes)
VALUES 
    (1, '2025-02-05', 'F000-0000', '高麗菜', 'M000-0000/ooxx資材', 10.0, '王小明', '間作及敷蓋稻草');

--  查詢其他資材使用紀錄
SELECT f.id, f.date_used, f.field_code, f.crop, f.material_code_or_name, f.usage_amount, f.operator, f.notes, u.username, u.farmer_name
FROM form12 f
JOIN users u ON f.user_id = u.id
WHERE f.crop = '高麗菜';


-- form13（其他資材與代碼對照表）
CREATE TABLE form13 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                            -- 關聯 `users` 表
    other_material_code VARCHAR(50),         -- 其他資材代碼
    other_material_name VARCHAR(255),        -- 其他資材名稱
    notes TEXT,                                       -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE  -- 外鍵，關聯 `users` 表
);

INSERT INTO form13 (user_id, other_material_code, other_material_name, notes)
VALUES 
    (1, 'M000-0000', 'ooxx資材', '間作及敷蓋稻草');
SELECT f.other_material_code, f.other_material_name, f.notes, u.username, u.farmer_name
FROM form13 f
JOIN users u ON f.user_id = u.id
WHERE f.other_material_name = 'ooxx資材';

-- form14（其他資材入出庫紀錄）
CREATE TABLE form14 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                             -- 關聯 `users` 表
    material_name VARCHAR(255),              -- 資材名稱
    manufacturer VARCHAR(255),                        -- 廠商
    supplier VARCHAR(255),                            -- 供應商
    packaging_unit VARCHAR(100),             -- 包裝單位
    packaging_volume VARCHAR(50),                     -- 包裝容量 (例如：公克、公斤、毫升、公升、其他)
    date DATE NULL,                               -- 日期
    purchase_quantity DECIMAL(10, 2),        -- 購入量 (例如：10公升)
    usage_quantity DECIMAL(10, 2),           -- 使用量 (例如：10公升)
    remaining_quantity DECIMAL(10, 2),       -- 剩餘量 (例如：10公升)
    notes TEXT,                                       -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE  -- 外鍵，關聯 `users` 表
);

-- 資料示例
INSERT INTO form14 (user_id, material_name, manufacturer, supplier, packaging_unit, packaging_volume, date, purchase_quantity, usage_quantity, remaining_quantity, notes)
VALUES 
    (1, 'ooxx資材', '廠商', '供應商', '包', '10公斤', '2025-02-05', 10.00, 5.00, 5.00, '無');
 
-- 查詢與 `users` 表關聯的其他資材入出庫紀錄
SELECT f.id, f.material_name, f.manufacturer, f.supplier, f.date, f.purchase_quantity, f.usage_quantity, f.remaining_quantity, u.username, u.farmer_name, f.notes
FROM form14 f
JOIN users u ON f.user_id = u.id
WHERE f.material_name = 'ooxx資材';






-- form15（場地設施之保養、維修及清潔管理紀錄）
CREATE TABLE form15 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                             -- 關聯 `users` 表
    date DATE NULL,                               -- 日期
    item VARCHAR(100),                       -- 項目
    operation VARCHAR(100),                  -- 作業內容
    recorder VARCHAR(255),                   -- 記錄人
    notes TEXT,                                       -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- 外鍵，關聯 `users` 表
);
-- 資料示例
INSERT INTO form15 (user_id, date, item, operation, recorder, notes)
VALUES 
    (1,  '2025-02-05', '育苗場所', '清潔', '王小明', '清理育苗場所的灰塵及雜物');
-- 查詢與 `users` 表關聯的作業記錄
SELECT f.id, f.date, f.item, f.operation, f.recorder, f.notes, u.username, u.farmer_name
FROM form15 f
JOIN users u ON f.user_id = u.id
WHERE f.item = '育苗場所';

-- form16（器具/機械/設備之保養、維修、校正及清潔管理紀錄）
CREATE TABLE form16 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                             -- 關聯 `users` 表
    date DATE NULL,                               -- 日期
    item VARCHAR(100),                       -- 項目
    operation VARCHAR(100),                  -- 作業內容
    recorder VARCHAR(255),                   -- 記錄人
    notes TEXT,                                       -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- 外鍵，關聯 `users` 表
);
-- 資料示例
INSERT INTO form16 (user_id, date, item, operation, recorder, notes)
VALUES 
    (1, '2025-02-05', '噴霧機', '保養', '王小明', '更換噴嘴，清洗濾網');

-- 查詢與 `users` 表關聯的作業記錄
SELECT f.id, f.date, f.item, f.operation, f.recorder, f.notes, u.username, u.farmer_name
FROM form16 f
JOIN users u ON f.user_id = u.id
WHERE f.item = '噴霧機';


-- form17（採收及採後處理紀錄）
CREATE TABLE form17 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                   -- 關聯 `users` 表
    harvest_date DATE NULL,                      -- 採收日期
    field_code VARCHAR(50),                 -- 田區代號
    crop_name VARCHAR(255),                 -- 作物名稱
    batch_or_trace_no VARCHAR(50),          -- 批次編號或履歷編號
    harvest_weight DECIMAL(10, 2),          -- 採收重量 (處理前)
    process_date DATE NULL,                      -- 處理日期
    post_harvest_treatment VARCHAR(100),    -- 採後處理內容
    post_treatment_weight DECIMAL(10, 2),   -- 處理後重量(公斤)

    verification_status VARCHAR(100),       -- 驗證狀態 
    notes TEXT,                             -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE    -- 外鍵，關聯 `users` 表
);
-- 資料示例
INSERT INTO form17 (user_id, harvest_date, field_code, crop_name, batch_or_trace_no, harvest_weight, process_date, post_harvest_treatment, post_treatment_weight, verification_status, notes)
VALUES 
    (1,  '2025-02-05', 'F000-0000', '高麗菜', 'ABCD-EFHG-IJKL', 10.00, '2025-02-06', '清洗', 9.50, '非驗證產品', '間作及敷蓋稻草');
-- 查詢與 `users` 表關聯的採收與處理記錄
SELECT f.id, f.harvest_date, f.crop_name, f.post_harvest_treatment, f.post_treatment_weight, f.verification_status, f.notes, u.username, u.farmer_name
FROM form17 f
JOIN users u ON f.user_id = u.id
WHERE f.crop_name = '高麗菜';


-- form18（乾燥作業紀錄）
CREATE TABLE form18 (
    id INT AUTO_INCREMENT PRIMARY KEY,                     -- 編號
    user_id INT NOT NULL,                            -- 關聯 `users` 表
    arena VARCHAR(255),                    -- 處理場所
    process_date DATE NULL,                     -- 處理日期
    item VARCHAR(255),                     -- 品項
    batch_number VARCHAR(50),              -- 批次編號
    fresh_weight DECIMAL(10, 2),           -- 鮮重 (公斤)
    operation TEXT,                                 -- 作業內容
    dry_weight DECIMAL(10, 2),             -- 乾重 (公斤)
    remarks TEXT,                                   -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- 外鍵，關聯 `users` 表
);
-- 插入資料範例
INSERT INTO form18 (user_id, arena, process_date, item, batch_number, fresh_weight, operation, dry_weight, remarks)
VALUES (1,  '高麗菜', '2025-02-05', '高麗菜', 'ABCD-EFHG-IJKL', 10.00, '金針浸泡___溶液:濃度__%__小時，金針漂水___分鐘，日曬___小時，乾燥___度C___小時', 9.00, '我是備註區');

-- 查詢與 `users` 表關聯的乾燥作業紀錄
SELECT f.id, f.process_date, f.item, f.dry_weight, f.remarks, u.username, u.farmer_name
FROM form18 f
JOIN users u ON f.user_id = u.id
WHERE f.item = '高麗菜';

-- form19（包裝及出貨紀錄）
CREATE TABLE form19 (
    id INT AUTO_INCREMENT PRIMARY KEY,                     -- 編號
    user_id INT NOT NULL,                            -- 關聯 `users` 表
    package VARCHAR(255),                   -- 包裝場所
    sale_date DATE NULL,                         -- 販售日期
    product_name VARCHAR(255),              -- 產品名稱
    sales_target TEXT,                      -- 銷售對象
    batch_number VARCHAR(50),               -- 批次編號
    shipment_quantity DECIMAL(10, 2),       -- 出貨量 (公斤)
    packaging_spec TEXT,                    -- 包裝規格
    label_usage_quantity INT,               -- 標章使用數量
    label_void_quantity INT,                -- 標章作廢數量
    verification_status VARCHAR(255),       -- 驗證狀態
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- 外鍵，關聯 `users` 表
);
-- 插入資料範例
INSERT INTO form19 (user_id, package, sale_date, product_name, sales_target, batch_number, shipment_quantity, packaging_spec, label_usage_quantity, label_void_quantity, verification_status)
VALUES (1,  'F000-0000', '2025-02-05', '高麗菜', '零售 (地點: ABC市場)', 'ABCD-EFHG-IJKL', 10.00, '包裝規格描述', 10, 0, '非驗證產品');

-- 查詢與 `users` 表關聯的包裝及出貨紀錄
SELECT f.id, f.sale_date, f.product_name, f.shipment_quantity, f.verification_status, u.username, u.farmer_name
FROM form19 f
JOIN users u ON f.user_id = u.id
WHERE f.product_name = '高麗菜';

-- form20（作業人員衛生及健康狀態檢查紀錄）
CREATE TABLE form20 (
    id INT AUTO_INCREMENT PRIMARY KEY,                     -- 編號
    user_id INT NOT NULL,                            -- 關聯 `users` 表
    checkitem TEXT,                         -- 檢查項目
    jobdate DATE NULL,                           -- 作業日期
    operator_name VARCHAR(255),             -- 作業人員姓名
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- 外鍵，關聯 `users` 表
);
-- 插入資料範例
INSERT INTO form20 (user_id, checkitem, jobdate, operator_name)
VALUES (1,  '共5項', '2025-02-05', '王小明');

-- 查詢與 `users` 表關聯的衛生及健康狀態檢查紀錄
SELECT f.id, f.jobdate, f.operator_name, f.checkitem, u.username, u.farmer_name
FROM form20 f
JOIN users u ON f.user_id = u.id;

-- form22（客戶抱怨/回饋紀錄）
CREATE TABLE form22 (
    id INT AUTO_INCREMENT PRIMARY KEY,                     -- 編號
    user_id INT NOT NULL,                            -- 關聯 `users` 表
    date DATE NULL,                              -- 日期
    customer_name VARCHAR(255),             -- 客戶名稱
    customer_phone VARCHAR(50),             -- 客戶電話
    complaint TEXT,                         -- 客訴內容
    resolution TEXT,                        -- 處理結果
    processor_name VARCHAR(255) ,           -- 處理人簽名
    processor_date DATE NULL,                    -- 處理日期
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- 外鍵，關聯 `users` 表
);

-- 插入資料範例
INSERT INTO form22 (user_id, date, customer_name, customer_phone, complaint, resolution,  processor_name, processor_date)
VALUES (1,  '2025-02-05', '王小明', '0988-888-888', '我是客訴內容區', '我是處理結果區', '王小明 (處理人)', '2025-02-06');

-- 查詢與 `users` 表關聯的客戶抱怨/回饋紀錄
SELECT f.id, f.date, f.customer_name, f.complaint, f.resolution, u.username, u.farmer_name, f.processor_name, f.processor_date
FROM form22 f
JOIN users u ON f.user_id = u.id;
