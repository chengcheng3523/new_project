// LoginForm 元件，負責處理使用者登入表單
import React ,{ useState, useContext, useEffect } from'react';
import AuthContext from '../auth/AuthContext';

const LoginForm = () => {
  const { login, isAuthenticated } = useContext(AuthContext);// 使用 AuthContext 來取得登入狀態與登入方法
  const [username, setUsername]= useState("")               // 狀態：儲存使用者輸入的帳號
  const [password, setPassword] = useState("");             // 狀態：儲存使用者輸入的密碼

  // 處理登入邏輯，呼叫 login 方法
  const handleLogin = () => {
    login(username, password).then(({token,error}) => {
        if (token) {
          alert('登入成功'); // 登入成功提示
        } else {
          alert(error || '登入失敗');// 登入失敗提示
        }
    });
  };

// 當使用者已登入，會自動導向首頁
useEffect(() => {
  if (isAuthenticated) {
    window.location.href = "/";  // 導向首頁
  }
}, [isAuthenticated]);

  return (
    <div className="container mt-5">
    <h1 className="mb-4">登入系統</h1>
    <div className="mb-3">
      <label htmlFor="username" className="form-label">使用者名稱</label>
      <input
        type="text"
        className="form-control"
        id="username"
        placeholder="請輸入帳號"
        value={username}
        onChange={(e) => setUsername(e.target.value)} // 更新帳號輸入值
      />
    </div>
    <div className="mb-3">
      <label htmlFor="password" className="form-label">密碼</label>
      <input
        type="password"
        className="form-control"
        id="password"
        placeholder="請輸入密碼"
        value={password}
        onChange={(e) => setPassword(e.target.value)} // 更新密碼輸入值
      />
    </div>
    <button onClick={handleLogin} className="btn btn-primary">登入</button>
    <button onClick={() => window.location.href = "/register"} className="btn btn-secondary ms-2">註冊</button>
  </div>
);
};

export default LoginForm;// 匯出 LoginForm 元件