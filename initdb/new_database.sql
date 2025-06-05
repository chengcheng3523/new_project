CREATE DATABASE IF NOT EXISTS t1;
USE t1;

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
    address     VARCHAR(200) COMMENT '住址',
    email       VARCHAR(50) COMMENT 'e-mail',
    total_area  DECIMAL(10,2) COMMENT '栽培總面積',
    notes       VARCHAR(50) COMMENT '備註',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- lands（農地資訊）
CREATE TABLE lands (
    id                 INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id            INT NOT NULL,                    -- 關聯 `users` 表
    number             VARCHAR(50) UNIQUE,            -- 農地編號
    lands_number       VARCHAR(50),            -- 農地地籍號碼
    area               DECIMAL(10,2),          -- 面積（單位：公頃）
    crop               VARCHAR(100),                    -- 種植作物
    notes              TEXT,                            -- 備註
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

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

-- form02（種子(苗)登記表）
CREATE TABLE form02 (
    id                   INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id              INT NOT NULL,                    -- 關聯 `users` 表
    lands_id         INT NOT NULL,                    -- 關聯 `lands` 表
    crop      VARCHAR(100),           -- 栽培作物
    crop_variety         VARCHAR(100),           -- 栽培品種
    seed_source          VARCHAR(255),           -- 種子(苗)來源
    seedling_purchase_date DATE NULL,                -- 育苗(購入)日期
    seedling_purchase_type VARCHAR(50),         -- 育苗(購入)種類
    notes                TEXT,                            -- 備註
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lands_id) REFERENCES lands(id) ON DELETE CASCADE
);

-- form03（栽培工作紀錄）
CREATE TABLE form03 (
    id                   INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id              INT NOT NULL,                    -- 關聯 `users` 表
    lands_id         INT NOT NULL,                    -- 關聯 `lands` 表
    operation_date       DATE NULL,                   -- 作業日期
    field_code           VARCHAR(50),            -- 田區代號
    crop                 VARCHAR(100),           -- 作物
    crop_content         TEXT,                   -- 作物內容（工作代碼及描述）
    notes                TEXT,                            -- 備註
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lands_id) REFERENCES lands(id) ON DELETE CASCADE
);

-- form06（肥料施用紀錄）
CREATE TABLE form06 (
    id                 INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id            INT NOT NULL,           -- 關聯 `users` 表
    lands_id         INT NOT NULL,                    -- 關聯 `lands` 表
    date_used          DATE NULL,           -- 使用日期
    field_code         VARCHAR(20),           -- 田區代號
    crop               VARCHAR(50),           -- 作物
    fertilizer_type    VARCHAR(100),           -- 施肥別 (基肥, 追肥)
    fertilizer_material_name VARCHAR(100),       -- 資材代碼或資材名稱
    fertilizer_amount  DECIMAL(10, 2),           -- 肥料使用量 (公斤/公升)
    dilution_factor    DECIMAL(5, 2),           -- 稀釋倍數 (液肥適用)
    operator           VARCHAR(100),           -- 操作人員
    process            TEXT,                            -- 製作流程
    notes              TEXT,                            -- 備註
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lands_id) REFERENCES lands(id) ON DELETE CASCADE
);

-- form07（肥料資材與代碼對照表）
CREATE TABLE form07 (
    id INT AUTO_INCREMENT PRIMARY KEY,                    -- 唯一編號
    user_id INT NOT NULL,                                  -- 關聯 `users` 表
    fertilizer_material_code VARCHAR(20) UNIQUE,          -- 肥料資材代碼
    fertilizer_material_name VARCHAR(100),         -- 肥料資材名稱
    manufacturer VARCHAR(100),                              -- 廠商
    supplier VARCHAR(100),                                  -- 供應商
    packaging_unit VARCHAR(100), -- 包裝單位□包 □瓶 □罐 □其他_______
    packaging_volume VARCHAR(50),                  -- 包裝容量，前面是數字，後面試單位選項（如：公克、公斤、毫升、公升等）
    notes TEXT,                                            -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,         -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    UNIQUE(fertilizer_material_code),                        -- 確保 `fertilizer_material_code` 是唯一的
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE    -- 外鍵，關聯 `users` 表
);

-- form08（肥料入出庫紀錄）
CREATE TABLE form08 (
    id INT AUTO_INCREMENT PRIMARY KEY,                     -- 編號，自動遞增
    user_id              INT NOT NULL,                    -- 關聯 `users` 表
    fertilizer_material_name VARCHAR(100),                    -- 資材名稱
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

-- form09（有害生物防治或環境消毒資材施用紀錄）
CREATE TABLE form09 (
    id INT AUTO_INCREMENT PRIMARY KEY,                        -- 編號，自動遞增
    user_id INT NOT NULL,                    -- 關聯 `users` 表
    lands_id         INT NOT NULL,                    -- 關聯 `lands` 表
    date_used DATE NULL,                                   -- 使用日期
    field_code VARCHAR(50),                            -- 田區代號
    crop VARCHAR(100),                                -- 作物名稱
    pest_target VARCHAR(100),                         -- 防治對象（如：蟲）
    pest_control_material_name VARCHAR(100),               -- 資材代碼或名稱
    water_volume DECIMAL(10, 2),                      -- 用水量（公升）
    chemical_usage DECIMAL(10, 2),                    -- 藥劑使用量（公斤、公升）
    dilution_factor DECIMAL(10, 2),                   -- 稀釋倍數
    safety_harvest_period INT,                        -- 安全採收期（天）
    operator_method VARCHAR(100),  -- 操作方式
    operator VARCHAR(100),                            -- 操作人員
    notes TEXT,                                                -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,            -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lands_id) REFERENCES lands(id) ON DELETE CASCADE
);

-- form10（防治資材與代碼對照表）
CREATE TABLE form10 (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id INT NOT NULL,               -- 關聯 `users` 表
    pest_control_material_code VARCHAR(100),   -- 防治資材代碼
    pest_control_material_name VARCHAR(100),   -- 防治資材名稱
    dosage_form VARCHAR(100),                        -- 劑型
    brand_name VARCHAR(100),                         -- 商品名(廠牌)
    supplier VARCHAR(100),                           -- 供應商
    packaging_unit VARCHAR(100),             -- 包裝單位
    packaging_volume VARCHAR(100),                  -- 包裝容量
    notes TEXT,                                              -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,          -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- form11（有害生物防治或環境消毒資材入出庫紀錄）
CREATE TABLE form11 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                             -- 關聯 `users` 表
    pest_control_material_name VARCHAR(255),              -- 資材名稱
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

-- form12（其他資材使用紀錄）
CREATE TABLE form12 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                             -- 關聯 `users` 表
    lands_id         INT NOT NULL,                    -- 關聯 `lands` 表
    date_used DATE NULL,                          -- 使用日期
    field_code VARCHAR(100),                 -- 田區代號
    crop VARCHAR(100),                       -- 作物名稱
    other_material_name VARCHAR(255),      -- 資材代碼或資材名稱
    usage_amount DECIMAL(10, 2),             -- 使用量
    operator VARCHAR(100),                   -- 操作人員
    notes TEXT,                                       -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lands_id) REFERENCES lands(id) ON DELETE CASCADE
);

-- form13（其他資材與代碼對照表）
CREATE TABLE form13 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                            -- 關聯 `users` 表
    other_material_code VARCHAR(50),         -- 其他資材代碼
    other_material_name VARCHAR(255),        -- 其他資材名稱
    manufacturer VARCHAR(255),                        -- 廠商
    supplier VARCHAR(255),                            -- 供應商
    packaging_unit VARCHAR(100),             -- 包裝單位
    packaging_volume VARCHAR(50),                     -- 包裝容量 (例如：公克、公斤、毫升、公升、其他)
    notes TEXT,                                       -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- 建立時間
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE  -- 外鍵，關聯 `users` 表
);

-- form14（其他資材入出庫紀錄）
CREATE TABLE form14 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                             -- 關聯 `users` 表
    other_material_name VARCHAR(255),              -- 資材名稱
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

-- form17（採收及採後處理紀錄）
CREATE TABLE form17 (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- 編號，自動遞增
    user_id INT NOT NULL,                   -- 關聯 `users` 表
    lands_id         INT NOT NULL,                    -- 關聯 `lands` 表
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lands_id) REFERENCES lands(id) ON DELETE CASCADE
);

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
