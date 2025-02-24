CREATE DATABASE IF NOT EXISTS new_database02;
USE new_database02;

-- users（使用者基本資料）
CREATE TABLE users(
    ID          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50) NOT NULL COMMENT '帳號',
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
    notes       TEXT        COMMENT '備註',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- land_parcels（農地資訊）
CREATE TABLE land_parcels (
    id                 INT AUTO_INCREMENT PRIMARY KEY,  -- 唯一編號
    user_id            INT NOT NULL,                    -- 關聯 `users` 表
    -- land_parcels 表中的 user_id 是手動指定的，並且必須是 users 表中已經存在的 id
    number             VARCHAR(50) NOT NULL,            -- 農地編號
    land_parcel_number VARCHAR(50) NOT NULL,            -- 農地地籍號碼
    area               DECIMAL(10,2) NOT NULL,          -- 面積（單位：公頃）
    crop               VARCHAR(100),                    -- 種植作物
    notes              TEXT,                            -- 備註
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 紀錄--
CREATE TABLE records (

    id                   INT AUTO_INCREMENT PRIMARY KEY,    -- 唯一編號，自動遞增
    field_code           VARCHAR(50) NOT NULL,              -- 田區代號
    crop                 VARCHAR(100) NOT NULL,             -- 作物
    crop_name VARCHAR(255) NOT NULL,                        -- 作物名稱

    user_id              INT NOT NULL,                      -- 關聯 `users` 表
    land_parcel_id       INT NOT NULL,                      -- 關聯 `land_parcels` 表

    date_used          DATE NOT NULL,                       -- 使用日期、作業日期、配製日期
    date DATE NOT NULL,                                     -- 日期
    material_code VARCHAR(100) NOT NULL,            -- 資材代碼
    material_name VARCHAR(255) NOT NULL,            -- 資材名稱
    operator           VARCHAR(100) ,                       -- 操作人員、配製人員名稱
    usage_amount         DECIMAL(10, 2) NOT NULL,           -- 使用量(公斤/公升)、肥料使用量、藥劑使用量、用水量（公升）
    operation TEXT,                                 -- 作業內容
    verification_status VARCHAR(255) NOT NULL,       -- 驗證狀態
    dilution_factor DECIMAL(10, 2) NOT NULL,                   -- 稀釋倍數

    area_code        VARCHAR(20) NOT NULL,            -- 場區代號
    area_size        DECIMAL(10,2) NOT NULL,          -- 場區面積（公頃）
    month            VARCHAR(10) NOT NULL,            -- 月份（1月-12月）
    crop_info        VARCHAR(255) NOT NULL,           -- 種植作物種類、產期、預估產量（公斤）
    cultivated_crop      VARCHAR(100) NOT NULL,           -- 栽培作物
    crop_variety         VARCHAR(100) NOT NULL,           -- 栽培品種
    seed_source          VARCHAR(255) NOT NULL,           -- 種子(苗)來源
    seedling_purchase_date DATE NOT NULL,                -- 育苗(購入)日期
    seedling_purchase_type VARCHAR(50) NOT NULL,         -- 育苗(購入)種類

    crop_content         TEXT NOT NULL,                   -- 作物內容（工作代碼及描述）
    preparation_process  TEXT,                            -- 配製流程簡述
    final_ph_value       DECIMAL(5, 2),                   -- 最終 pH 值
    final_ec_value       DECIMAL(5, 2),                   -- 最終 EC 值(mS/cm)
    fertilizer_type    ENUM('基肥', '追肥') NOT NULL,  -- 施肥別 (基肥, 追肥)
    process            TEXT,                            -- 製作流程
    pest_target VARCHAR(100) NOT NULL,                         -- 防治對象（如：蟲）
    safety_harvest_period INT NOT NULL,                        -- 安全採收期（天）
    operator_method ENUM('噴灑', '撒施', '灌注', '其他') NOT NULL, -- 操作方式
    harvest_date DATE NOT NULL,                     -- 採收日期
    harvest_weight DECIMAL(10, 2) NOT NULL,         -- 採收重量 (處理前)
    process_date DATE NOT NULL,                     -- 處理日期
    post_harvest_treatment ENUM('清洗', '整修', '去雜', '分級', '預冷', '冷藏', '去殼/去莢', '其他') NOT NULL,  -- 採後處理內容
    post_treatment_weight DECIMAL(10, 2) NOT NULL,  -- 處理後重量
    verification_organization VARCHAR(255),         -- 驗證機構

    manufacturer VARCHAR(100),                                 -- 廠商
    supplier VARCHAR(100),                                     -- 供應商
    packaging_unit ENUM('包', '瓶', '罐', '其他') NOT NULL,     -- 包裝單位
    purchase_quantity DECIMAL(10, 2) NOT NULL,                 -- 購入量
    usage_quantity DECIMAL(10, 2) NOT NULL,                    -- 使用量
    remaining_quantity DECIMAL(10, 2) NOT NULL,                -- 剩餘量
    packaging_volume VARCHAR(50),                              -- 包裝容量 (例如：公克 .公斤 .毫升 .公升 .其他)
    recorder VARCHAR(255) NOT NULL,                             -- 記錄人
    dosage_form VARCHAR(100),                                   -- 劑型
    brand_name VARCHAR(100),                                    -- 商品名(廠牌)
    item VARCHAR(100), -- 項目、品項

    batch_number VARCHAR(50) NOT NULL,              -- 批次編號
    arena VARCHAR(255) NOT NULL,                    -- 處理場所
    fresh_weight DECIMAL(10, 2) NOT NULL,           -- 鮮重 (公斤)
    dry_weight DECIMAL(10, 2) NOT NULL,             -- 乾重 (公斤)
    package VARCHAR(255) NOT NULL,                   -- 包裝場所
    sale_date DATE NOT NULL,                         -- 販售日期
    product_name VARCHAR(255) NOT NULL,              -- 產品名稱
    sales_target TEXT NOT NULL,                      -- 銷售對象
    shipment_quantity DECIMAL(10, 2) NOT NULL,       -- 出貨量 (公斤)
    packaging_spec TEXT NOT NULL,                    -- 包裝規格
    label_usage_quantity INT NOT NULL,               -- 標章使用數量
    label_void_quantity INT NOT NULL,                -- 標章作廢數量

    checkitem TEXT NOT NULL,                         -- 檢查項目
    jobdate DATE NOT NULL,                           -- 作業日期
    customer_name VARCHAR(255) NOT NULL,             -- 客戶名稱
    customer_phone VARCHAR(50) NOT NULL,             -- 客戶電話
    complaint TEXT NOT NULL,                         -- 客訴內容
    resolution TEXT NOT NULL,                        -- 處理結果
    processor VARCHAR(255) NOT NULL,                 -- 處理人簽名/日期

    notes                TEXT,                              -- 備註
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,-- 建立時間
    updated_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,-- 更新時間
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (land_parcel_id) REFERENCES land_parcels(id) ON DELETE CASCADE
);

CREATE TABLE material (
    id INT AUTO_INCREMENT PRIMARY KEY,                      -- 編號，自動遞增
    nutrient_material_code VARCHAR(20) UNIQUE ,         -- 養液配製資材代碼
    nutrient_material_name VARCHAR(100) NOT NULL,           -- 養液配製資材名稱
    fertilizer_material_code VARCHAR(20) UNIQUE ,       -- 肥料資材代碼
    fertilizer_material_name VARCHAR(100) NOT NULL,         -- 肥料資材名稱
    pest_control_material_code VARCHAR(100) UNIQUE ,    -- 防治資材代碼
    pest_control_material_name VARCHAR(100) NOT NULL,       -- 防治資材名稱
    other_material_code VARCHAR(50) UNIQUE ,            -- 其他資材代碼
    other_material_name VARCHAR(255) NOT NULL,              -- 其他資材名稱
    notes                 TEXT                             -- 備註
);
