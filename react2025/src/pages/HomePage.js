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
  const [selectedForm, setSelectedForm] = useState(null);
  const [formData, setFormData] = useState(null); // 用來儲存從API獲得的資料


// 這個函數用於向後端 API 請求資料

const fetchFormData = async (formName) => {
  try {
    setFormData(null);  // 清空之前的資料
    const response = await fetch(`http://127.0.0.1:5000/api/${formName}`);
    const data = await response.json();
    setFormData(data);  // 設定資料
    return JSON.stringify(data);
  } catch (error) {
    console.error('API 請求失敗:', error);
    return '資料加載失敗';
  }
};

  // 動態渲染表格
  const renderTable = () => {
    if (!formData) return null;
  
    if (typeof formData === 'string') {
      return <p>{formData}</p>;  // 顯示錯誤訊息
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
            <th key={index}>{header}</th>
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

  const handleCardClick = async (title) => {

    let formData = null;
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
          <TitleCard title="肥料資材與代碼" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page08')}>
          <TitleCard title="肥料入出庫" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page09')}>
          <TitleCard title="有害生物防治或環境消毒資材施用" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page10')}>
          <TitleCard title="防治資材與代碼" />
        </ProductContainer>

        <ProductContainer onClick={() => handleCardClick('Page11')}>
          <TitleCard title="有害生物防治或環境消毒資材入出庫" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page12')}>
          <TitleCard title="其他資材使用" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page13')}>
          <TitleCard title="其他資材與代碼" />
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

      <UnitConverter />
      
      <div>
        {/* {selectedForm} */} {/* 表格內容確認 */}
        {renderTable()} {/* 顯示動態生成的表格 */}
      </div>

      


     </DefaultLayout>

    );
};
export default HomePage;
