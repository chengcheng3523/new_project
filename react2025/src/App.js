// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CartPage from './pages/CartPage';
import CheckoutPage from './pages/CheckoutPage';
import ProductCollectionPage from './pages/ProductCollectionPage';
import ProductPage from './pages/ProductPage';
import {AuthProvider} from './components/auth/AuthContext'; // 確保正確導入 AuthProvider
import './index.css'; 
import LoginPage from './pages/LoginPage';
import ScrollToTop from './components/common/ScrollToTop';

import RegisterPage from './pages/RegisterPage';
import Lands from './Form-Page/Lands'; // 土地資料


import Page001 from './Form-Page/Page001'; // 表1-1
import Page02 from './Form-Page/Page02'; // 表1-2 未完成
import Page002 from './Form-Page/Page002'; // 表2
import Page03 from './Form-Page/Page03'; // 表3
import Page04 from './Form-Page/Page04'; // 表4
import Page05 from './Form-Page/Page05'; // 表5
import Page06 from './Form-Page/Page06'; // 表6
import Page07 from './Form-Page/Page07'; // 表7
import Page08 from './Form-Page/Page08'; // 表8
import Page09 from './Form-Page/Page09'; // 表9
import Page10 from './Form-Page/Page10'; // 表10

import Page11 from './Form-Page/Page11'; // 表11
import Page12 from './Form-Page/Page12'; // 表12
import Page13 from './Form-Page/Page13'; // 表13
import Page14 from './Form-Page/Page14'; // 表14
import Page15 from './Form-Page/Page15'; // 表15
import Page16 from './Form-Page/Page16'; // 表16
import Page17 from './Form-Page/Page17'; // 表17
import Page18 from './Form-Page/Page18'; // 表18
import Page19 from './Form-Page/Page19'; // 表19
import Page20 from './Form-Page/Page20'; // 表20
import Page22 from './Form-Page/Page22'; // 表22


const App = () => {
  return (
     <AuthProvider>
      <BrowserRouter>
      <ScrollToTop />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/mall" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/mall/:categoryname" element={<ProductCollectionPage />} />
          <Route path="/:productname" element={<ProductPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route path="/Lands" element={< Lands />} />
          <Route path="/Page001" element={< Page001 />} />  
          <Route path="/Page02" element={< Page02 />} />
          <Route path="/Page002" element={< Page002 />} />
          <Route path="/Page03" element={< Page03 />} />

          <Route path="/Page04" element={< Page04 />} />
          <Route path="/Page05" element={< Page05 />} />
          <Route path="/Page06" element={< Page06 />} />
          <Route path="/Page07" element={< Page07 />} />
          <Route path="/Page08" element={< Page08 />} />
          <Route path="/Page09" element={< Page09 />} />
          <Route path="/Page10" element={< Page10 />} />

          <Route path="/Page11" element={< Page11 />} />
          <Route path="/Page12" element={< Page12 />} />
          <Route path="/Page13" element={< Page13 />} />
          <Route path="/Page14" element={< Page14 />} />
          <Route path="/Page15" element={< Page15 />} />
          <Route path="/Page16" element={< Page16 />} />
          <Route path="/Page17" element={< Page17 />} />
          <Route path="/Page18" element={< Page18 />} />
          <Route path="/Page19" element={< Page19 />} />
          <Route path="/Page20" element={< Page20 />} />
          
          <Route path="/Page22" element={< Page22 />} />


        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;