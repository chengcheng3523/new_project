import React ,{ useState, useContext } from 'react';
import DefaultLayout from '../components/layout/DefaultLayout';
import Clearfix from '../components/common/Clearfix';
import styled from 'styled-components';
import TitleCard from '../components/product/TitleCard.js';
import AuthContext from '../components/auth/AuthContext.js';
import UnitConverter from '../components/layout/UnitConverter';

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
    if (title === 'Page001') {
      setSelectedForm(isAuthenticated ? <Page001 /> : <div>資料: Page001</div>);

    } else if (title === 'Lands') {
      setSelectedForm(isAuthenticated ? <Lands /> : <div>資料: Lands</div>);
    } else if (title === 'Page002') {
      setSelectedForm(isAuthenticated ? <Page002 /> : <div>資料: Page002</div>);
    } else if (title === 'Page02') {
      setSelectedForm(isAuthenticated ? <Page02 /> : <div>資料: Page02</div>);
    } else if (title === 'Page03') {
      setSelectedForm(isAuthenticated ? <Page03 /> : <div>資料: Page03</div>);

    } else if (title === 'Page06') {
      setSelectedForm(isAuthenticated ? <Page06 /> : <div>資料: Page06</div>);
    } else if (title === 'Page07') {
      setSelectedForm(isAuthenticated ? <Page07 /> : <div>資料: Page07</div>);
    } else if (title === 'Page08') {
      setSelectedForm(isAuthenticated ? <Page08 /> : <div>資料: Page08</div>);
    } else if (title === 'Page09') {
      setSelectedForm(isAuthenticated ? <Page09 /> : <div>資料: Page09</div>);
    } else if (title === 'Page10') {
      setSelectedForm(isAuthenticated ? <Page10 /> : <div>資料: Page10</div>);

    } else if (title === 'Page11') {
      setSelectedForm(isAuthenticated ? <Page11 /> : <div>資料: Page11</div>);
    } else if (title === 'Page12') {
      setSelectedForm(isAuthenticated ? <Page12 /> : <div>資料: Page12</div>);
    } else if (title === 'Page13') {
      setSelectedForm(isAuthenticated ? <Page13 /> : <div>資料: Page13</div>);
    } else if (title === 'Page14') {
      setSelectedForm(isAuthenticated ? <Page14 /> : <div>資料: Page14</div>);
    } else if (title === 'Page15') {
      setSelectedForm(isAuthenticated ? <Page15 /> : <div>資料: Page15</div>);
    } else if (title === 'Page16') {
      setSelectedForm(isAuthenticated ? <Page16 /> : <div>資料: Page16</div>);
    } else if (title === 'Page17') {
      setSelectedForm(isAuthenticated ? <Page17 /> : <div>資料: Page17</div>);

    } else if (title === 'Page22') {
      setSelectedForm(isAuthenticated ? <Page22 /> : <div>資料: Page22</div>);

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
        {selectedForm}
      </div>


     </DefaultLayout>

    );
};
export default HomePage;
