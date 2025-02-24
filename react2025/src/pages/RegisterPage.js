// src/pages/RegisterPage.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import Container from '../components/common/Container';

// 自訂登入框的樣式，設定背景為白色
const StyledLoginBox =styled.div`
  background-color: white;
`;

// 自訂容器樣式，設定排版為左右分佈並加入內邊距
const StyledLoginContainer =styled(Container)`
  display: flex;
  justify-content: space-between;
  padding: 48px 0;
`;

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    plain_password: '',
    unit_name: '',
    farmer_name: '',
    phone: '',
    fax: '',
    mobile: '',
    address: '',
    email: '',
    total_area: '0',
    notes: '',
    land_parcel_id: "LP123"
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // await createUser(formData);
      // 將註冊資料儲存在 localStorage 中
      // const users = JSON.parse(localStorage.getItem('users')) || [];
      // users.push(formData);
      // localStorage.setItem('users', JSON.stringify(users));
      const payload = { 
        ...formData, 
        plain_password: formData.password // 確保 plain_password 與 password 一致
    };
      const response = await axios.post('http://127.0.0.1:5000/api/users/post', payload);
      if (response.status === 201) {
      alert('註冊成功');
      navigate('/login'); 
      }
    } catch (error) {
      console.error('註冊失敗', error);
      alert('註冊失敗，請檢查輸入資料或稍後再試');
    }
  };

  return (
    <StyledLoginBox> {/* 登入框，背景為白色 */}
        <StyledLoginContainer> {/* 彈性容器，內容左右分佈 */}
        <div className="container mt-5">
      <h1 className="mb-4">註冊帳號</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">帳號</label>
          <input name="username" className="form-control" placeholder="請輸入帳號" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">密碼</label>
          <input name="password" type="password" className="form-control" placeholder="請輸入密碼" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">單位名稱</label>
          <input name="unit_name" className="form-control" placeholder="請輸入單位名稱" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">農友姓名</label>
          <input name="farmer_name" className="form-control" placeholder="請輸入農友姓名" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">電話</label>
          <input name="phone" className="form-control" placeholder="請輸入電話" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">傳真</label>
          <input name="fax" className="form-control" placeholder="請輸入傳真" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">手機</label>
          <input name="mobile" className="form-control" placeholder="請輸入手機" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">地址</label>
          <input name="address" className="form-control" placeholder="請輸入地址" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">電子郵件</label>
          <input name="email" className="form-control" placeholder="請輸入電子郵件" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">田地編號</label>
          <input name="land_parcel_id" className="form-control" placeholder="請輸入田地編號" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">總面積</label>
          <input name="total_area" className="form-control" placeholder="請輸入總面積" onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label className="form-label">備註</label>
          <input name="notes" className="form-control" placeholder="請輸入備註" onChange={handleChange} />
        </div>


        <button type="submit" className="btn btn-primary">註冊</button>
        <button type="button" onClick={() => navigate('/login')} className="btn btn-secondary ms-2">返回登入</button>
      </form>
    </div>
    </StyledLoginContainer>
    </StyledLoginBox>
  );
};

export default RegisterPage;