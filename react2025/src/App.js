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





        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;