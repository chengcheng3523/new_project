import React ,{ useState, useContext } from 'react';
import DefaultLayout from '../components/layout/DefaultLayout';
import Clearfix from '../components/common/Clearfix';
import styled from 'styled-components';
import TitleCard from '../components/product/TitleCard.js';
import AuthContext from '../components/auth/AuthContext.js';
import Page01 from '../Form-Page/Page01';
import Page02 from '../Form-Page/Page02';
import Page002 from '../Form-Page/Page002';
import Page003 from '../Form-Page/Page003';
// import Page004 from '../Form-Page/Page004';
// import Page005 from '../Form-Page/Page005';
// import Page006 from '../Form-Page/Page006';





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

  const [selectedForm, setSelectedForm] = useState(null);

  const handleCardClick = (title) => {
    if (title === 'Page01') {
      setSelectedForm(isAuthenticated ? <Page01 /> : <div>資料紀錄: Page01</div>);
    } else if (title === 'Page02') {
      setSelectedForm(isAuthenticated ? <Page02 /> : <div>資料紀錄: Page02</div>);
    } else if (title === 'Page002') {
      setSelectedForm(isAuthenticated ? <Page002 /> : <div>資料紀錄: Page002</div>);
    } else if (title === 'Page003') {
      setSelectedForm(isAuthenticated ? <Page003 /> : <div>資料紀錄: Page003</div>);
    } else {
      setSelectedForm(null);
    }
  };

    return  (
     <DefaultLayout fixedHeader>{/* 使用預設佈局，確保頁面一致性 */}
      總覽頁面
      <Clearfix /> {/* 清除浮動 */}
      {isAuthenticated && <h1>歡迎回來</h1>} {/* 如果已登入，顯示歡迎訊息 */}
      
      <ProductCollectionContainer>
        <ProductContainer onClick={() => handleCardClick('Page01')}>
          <TitleCard title="使用者基本資料" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page02')}>
          <TitleCard title="生產計畫" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page002')}>
          <TitleCard title="種子(苗)紀錄" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page003')}>
          <TitleCard title="栽培工作" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page004')}>
          <TitleCard title="養液配製" />
        </ProductContainer>
        <ProductContainer onClick={() => handleCardClick('Page005')}>
          <TitleCard title="資材與代碼對照表" />
        </ProductContainer>
      </ProductCollectionContainer>

      <div>
        {selectedForm}
      </div>

     </DefaultLayout>
    );
};
export default HomePage;  
