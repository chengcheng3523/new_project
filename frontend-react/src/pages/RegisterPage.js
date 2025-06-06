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
    plain_password: ''
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
      // 前端驗證：檢查密碼是否一致
    if (formData.password !== formData.plain_password) {
      alert("密碼與確認密碼不一致");
      return;
    }
    try {
      const payload = { 
        username: formData.username, 
        password: formData.password,
        plain_password: formData.plain_password
      };
  
      const response = await axios.post('http://127.0.0.1:5000/api/register/post', payload);
      
      if (response.status === 201) {
        alert('註冊成功');
        localStorage.setItem('user_id', response.data.user_id); // 存 user_id
        navigate('/login'); // 跳轉到的頁面
      }
    } catch (error) {
      console.error('註冊失敗', error);
      if (error.response && error.response.data.error) {
        alert(error.response.data.error); // 顯示後端錯誤訊息
      } else {
        alert('註冊失敗，請稍後再試');
      }
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
          <label className="form-label">確認密碼</label>
          <input name="plain_password" type="password" className="form-control" placeholder="請再次輸入密碼" onChange={handleChange} />
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