import React ,{ useState, useContext } from 'react';
import DefaultLayout from '../components/layout/DefaultLayout';
import Clearfix from '../components/common/Clearfix';
import styled from 'styled-components';
import TitleCard from '../components/product/TitleCard.js';
import AuthContext from '../components/auth/AuthContext.js';
import UnitConverter from '../components/layout/UnitConverter';
// import axios from 'axios';

import Lands from '../Form-Page/Lands';
import Page001 from '../Form-Page/Page001';
import Page02 from '../Form-Page/Page02';
import Page002 from '../Form-Page/Page002';
import Page03 from '../Form-Page/Page03';

import Page06 from '../Form-Page/Page06';
import Page07 from '../Form-Page/Page07';
import Page08 from '../Form-Page/Page08';
import Page09 from '../Form-Page/Page09';
import Page10 from '../Form-Page/Page10';

import Page11 from '../Form-Page/Page11';
import Page12 from '../Form-Page/Page12';
import Page13 from '../Form-Page/Page13'; 
import Page14 from '../Form-Page/Page14';
import Page15 from '../Form-Page/Page15';
import Page16 from '../Form-Page/Page16';
import Page17 from '../Form-Page/Page17';
// import Page18 from '../Form-Page/Page18';
// import Page19 from '../Form-Page/Page19';
// import Page20 from '../Form-Page/Page20';

import Page22 from '../Form-Page/Page22';

// LoadingText 樣式元件定義
const LoadingText = styled.p`
  font-size: 18px;
  color: #555;
  text-align: center;
  margin: 20px 0;
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  th, td {
    padding: 8px;
    border: 1px solid #ddd;
  }
  th {
    background-color: #f2f2f2;
  }
`;

// ProductCollectionContainer 元件，用於包裝產品集合區域
const ProductCollectionContainer = styled.div`
 margin: 0 -4px 48px -4px;
 width: 100%;
 display:flex;
 flex-wrap: wrap;
`;
// ProductContainer 元件，用於包裝每個產品
const ProductContainer = styled.div`
  padding: 4px;
  width: calc(100% - 8px); /* 默認顯示一個一排，考慮到間距 */
  box-sizing: border-box; /* 確保 padding 包含在寬度內 */
  
  @media (min-width: 577px) {
    width: calc(50% - 8px); /* 中等螢幕顯示兩個一排，考慮到間距 */
  }
  
  @media (min-width: 769px) {
    width: calc(20% - 8px); /* 桌機版顯示五個一排，考慮到間距 */
  }
`;

const HomePage =()=> {
  // 使用 AuthContext 來取得登入狀態
  const{ isAuthenticated } = useContext(AuthContext);
  // 使用 useState 來管理選擇的表單狀態
  // eslint-disable-next-line no-unused-vars
  const [selectedForm, setSelectedForm] = useState(null);
  const [formData, setFormData] = useState(null); // 用來儲存從API獲得的資料
  const [loading, setLoading] = useState(false);
  // 請求前 setLoading(true)，請求後 setLoading(false)

// 這個函數用於向後端 API 請求資料

const fetchFormData = async (formName) => {
  try {
    setLoading(true);  // 開始載入
    // setFormData(null);  // 清空之前的資料
    const response = await fetch(`http://127.0.0.1:5000/api/${formName}`);
    const data = await response.json();
    setFormData(data);  // 設定資料
    return JSON.stringify(data);
  } catch (error) {
    console.error('API 請求失敗:', error);
    return '資料加載失敗';
  } finally {
    setLoading(false);  // 載入結束
  }
};

  // 動態渲染表格
  const renderTable = () => {
    if (!formData) return null;
  
    if (typeof formData === 'string') {
      if (!Array.isArray(formData)) return <p>資料格式錯誤</p>;
      
      // return <p>{formData}</p>;  // 顯示錯誤訊息
    }

  const headers = Object.keys(formData[0]);

  // 假設我們根據某個欄位排序 formData，例如按 name 排序
  const sortedData = [...formData].sort((a, b) => {
    if (a.id < b.id) return -1;
    if (a.id > b.id) return 1;
    return 0;
  });

  return (
    <Table>
      <thead>
        <tr>
          {headers.map((header, index) => (
            <th key={index}>{columnNameMap[header] || header}</th>
            // <th key={index}>{header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sortedData.map((row, index) => (
          <tr key={index}>
            {headers.map((header, headerIndex) => (
              <td key={headerIndex}>{row[header]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

const columnNameMap = {
  id: 'ID',
  username: '帳號',
  password: '密碼',
  unit_name: '單位名稱',
  farmer_name: '經營農戶姓名',
  phone: '聯絡電話',
  fax: '傳真',
  mobile: '行動電話',
  address: '地址',
  email: '電子郵件(EMAIL)',
  total_area: '栽培總面積',
  notes: '備註',
  created_at: '建立時間',
  updated_at: '更新時間',
  user_id: '使用者ID',
  land_id: '農地ID',
  number: '農地編號',
  field_code: '田區代號',
  lands_number: '農地地籍號碼',
  area: '面積(單位：公頃)',
  crop: '作物',
  crop_name: '作物名稱',
  land_parcel_id: '農地地籍ID',
  date_used: '使用日期',
  operation_date: '作業日期',
  chemical_usage:'藥劑使用量（公斤/公升）',
  water_volume:'用水量（公升）',
  fertilizer_amount:'肥料使用量（公斤/公升）',
  date: '日期',
  material_code: '資材代號',
  material_name: '資材名稱',
  operator: '操作人員、配製人員名稱',
  usage_amount:'使用量',
  operation: '作業內容',
  verification_status:'驗證狀態',
  dilution_factor: '稀釋倍數',
  area_code:'場區代號',
  area_size: '場區面積(公頃)',
  month:'月份',
  crop_info:'種植作物種類、產期、預估產量（公斤）',
  cultivated_crop: '栽培作物',
  crop_variety:'栽培品種',
  seed_source:'種子(苗)來源',
  seedling_purchase_date:'育苗(購入)日期',
  seedling_purchase_type:'育苗(購入)種類',

  crop_content:'作物內容（工作代號及描述',
  preparation_process:'配製流程簡述',
  final_ph_value:'最終pH值',
  final_ec_value:'最終EC值(mS/cm)',
  fertilizer_type:'施肥別(基肥、追肥)',
  process:'製作流程',
  pest_target:'防治對象（如：蟲）',
  safety_harvest_period:'安全採收期（天）',
  operator_method:'操作方式',
  harvest_date:'採收日期',
  harvest_weight:'採收重量(處理前)',
  process_date:'處理日期',
  post_harvest_treatment:'採後處理內容',
  post_treatment_weight:'處理後重量',
  verification_organization:'驗證機構',

  manufacturer:'廠商',
  supplier:'供應商',
  packaging_unit:'包裝單位',
  purchase_quantity:'購入量',
  usage_quantity:'使用量',
  remaining_quantity:'剩餘量',
  packaging_volume:'包裝容量 (例如：公克、公斤、毫升、公升、其他)',
  recorder:'記錄人',
  dosage_form:'劑型',
  brand_name:'商品名(廠牌)',
  item:'項目、品項',
  processor_date:'處理日期',
  processor_name:'處理人簽名',
  batch_number:'批次編號',
  arena:'處理場所',
  fresh_weight:'鮮重 (公斤)',
  dry_weight:'乾重 (公斤)',
  package:'包裝場所',
  sale_date:'販售日期',
  product_name:'產品名稱',
  sales_target:'銷售對象',
  shipment_quantity:'出貨量 (公斤)',
  packaging_spec:'包裝規格',
  label_usage_quantity:'標章使用數量',
  label_void_quantity:'標章作廢數量',

  batch_or_trace_no:'批次編號或履歷編號',
  checkitem:'檢查項目',
  jobdate:'作業日期',
  customer_name:'客戶名稱',
  customer_phone:'客戶電話',
  complaint:'客訴內容',
  resolution:'處理結果',
  processor:'處理人簽名/日期',
  fertilizer_material_code:'肥料資材代號',
  fertilizer_material_name:'肥料資材名稱',
  pest_control_material_code:'防治資材代號',
  pest_control_material_name:'防治資材名稱',
  other_material_code:'其他資材代號',
  other_material_name:'其他資材名稱',
  // 依你的資料結構加入更多對應
};

  const handleCardClick = async (title) => {

    // let formData = null;
    // 根據 title 來決定要載入的表單
    if (title === 'Page001') {
      setSelectedForm(isAuthenticated ? <Page001 /> : await fetchFormData('users/get'));

    } else if (title === 'Lands') {
      setSelectedForm(isAuthenticated ? <Lands /> : await fetchFormData('lands'));
    } else if (title === 'Page002') {
      setSelectedForm(isAuthenticated ? <Page002 /> : await fetchFormData('form002'));
    } else if (title === 'Page02') {
      setSelectedForm(isAuthenticated ? <Page02 /> : await fetchFormData('form02'));
    } else if (title === 'Page03') {
      setSelectedForm(isAuthenticated ? <Page03 /> : await fetchFormData('form03'));

    } else if (title === 'Page06') {
      setSelectedForm(isAuthenticated ? <Page06 /> : await fetchFormData('form06'));
    } else if (title === 'Page07') {
      setSelectedForm(isAuthenticated ? <Page07 /> : await fetchFormData('form07'));
    } else if (title === 'Page08') {
      setSelectedForm(isAuthenticated ? <Page08 /> : await fetchFormData('form08'));
    } else if (title === 'Page09') {
      setSelectedForm(isAuthenticated ? <Page09 /> : await fetchFormData('form09'));
    } else if (title === 'Page10') {
      setSelectedForm(isAuthenticated ? <Page10 /> : await fetchFormData('form10'));

    } else if (title === 'Page11') {
      setSelectedForm(isAuthenticated ? <Page11 /> : await fetchFormData('form11'));
    } else if (title === 'Page12') {
      setSelectedForm(isAuthenticated ? <Page12 /> : await fetchFormData('form12'));
    } else if (title === 'Page13') {
      setSelectedForm(isAuthenticated ? <Page13 /> : await fetchFormData('form13'));
    } else if (title === 'Page14') {
      setSelectedForm(isAuthenticated ? <Page14 /> : await fetchFormData('form14'));
    } else if (title === 'Page15') {
      setSelectedForm(isAuthenticated ? <Page15 /> : await fetchFormData('form15'));
    } else if (title === 'Page16') {
      setSelectedForm(isAuthenticated ? <Page16 /> : await fetchFormData('form16'));
    } else if (title === 'Page17') {
      setSelectedForm(isAuthenticated ? <Page17 /> : await fetchFormData('form17'));

    } else if (title === 'Page22') {
      setSelectedForm(isAuthenticated ? <Page22 /> : await fetchFormData('form22'));

    } else {
      setSelectedForm(null);
  
      setSelectedForm(formData); // 設定選中的表單內容
    }
  };

    return  (
     <DefaultLayout fixedHeader>{/* 使用預設佈局，確保頁面一致性 */}
      總覽頁面
      <Clearfix /> {/* 清除浮動 */}
      {isAuthenticated && <h1>歡迎回來</h1>} {/* 如果已登入，顯示歡迎訊息 */}
      
      <ProductCollectionContainer>
        <ProductContainer onClick={() => handleCardClick('Page001')}>
          <TitleCard title="使用者基本資料" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Lands')}>
          <TitleCard title="農地資訊" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page002')}>
          <TitleCard title="生產計畫" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page02')}>
          <TitleCard title="種子(苗)登記" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page03')}>
          <TitleCard title="栽培工作" />
        </ProductContainer>

        <ProductContainer onClick={() => handleCardClick('Page06')}>
          <TitleCard title="肥料施用" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page07')}>
          <TitleCard title="肥料資材與代號" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page08')}>
          <TitleCard title="肥料入出庫" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page09')}>
          <TitleCard title="有害生物防治或環境消毒資材施用" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page10')}>
          <TitleCard title="防治資材與代號" />
        </ProductContainer>

        <ProductContainer onClick={() => handleCardClick('Page11')}>
          <TitleCard title="有害生物防治或環境消毒資材入出庫" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page12')}>
          <TitleCard title="其他資材使用" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page13')}>
          <TitleCard title="其他資材與代號" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page14')}>
          <TitleCard title="其他資材入出庫" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page15')}>
          <TitleCard title="場地設施之保養、維修及清潔管理" />
        </ProductContainer>

        <ProductContainer onClick={() => handleCardClick('Page16')}>
          <TitleCard title="器具/機械/設備之保養、維修、校正及清潔管理" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page17')}>
          <TitleCard title="採收及採後處理" />
        </ProductContainer>

        <ProductContainer onClick={() => handleCardClick('Page22')}>
          <TitleCard title="客戶抱怨/回饋" />
        </ProductContainer>
      </ProductCollectionContainer>
      

      {loading && <LoadingText>資料載入中...</LoadingText>}
      {isAuthenticated && selectedForm} {/* 僅在已登入時渲染 selectedForm */}
      {renderTable()} {/* 顯示動態生成的表格 */}

      <UnitConverter /> {/* 單位轉換器 */}

     </DefaultLayout>

    );
};
export default HomePage;
