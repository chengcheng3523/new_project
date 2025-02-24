import React, { useState, createContext, useEffect } from "react";
import { jwtDecode } from 'jwt-decode';

const defaultContextValue = {
  isAuthenticated: false,
  userId: null,
  unitName: "",
  role: "guest",
};

const AuthContext = createContext(defaultContextValue);


export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setInAuthenticated] = useState(
    defaultContextValue.isAuthenticated
  ); // 狀態：判斷使用者是否已登入
  const [userId, setUserId] = useState(defaultContextValue.userId); // 狀態：儲存登入後的使用者 ID
  const [unitName, setUnitName] = useState(defaultContextValue.unitName); // 狀態：儲存登入後的單位名稱
  const [role, setRole] = useState(defaultContextValue.role);

  useEffect(() => {
    try {
      const authState = JSON.parse(localStorage.getItem("shopee:auth.state"));
      const token = localStorage.getItem("shopee:auth.token");
      if (authState && authState.token) {
        setInAuthenticated(true);
        setUserId(authState.userId);
        setUnitName(authState.unitName);
        setRole(authState.role || "user");
      } else if (token) {
        const decoded = jwtDecode(token); // 解析 JWT token
        setInAuthenticated(true); // 設定為已登入
        setUserId(decoded.userId); // 載入儲存的使用者 ID
        setRole(decoded.role); // 載入儲存的角色
      }
    } catch (error) {
      console.error("Failed to parse auth state from localStorage", error);
    }
  }, []);

  const filterDataByRole = (data) => {
    return role === "admin"
      ? data
      : data.filter((item) => item.user_id === userId);
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        userId,
        unitName,
        role,

        // 登入方法，透過 API 進行身份驗證
        login: async (username, password) => {
          if (!username || !password) {
            return { token: null, error: "請輸入帳號和密碼" };
          }
          try {
            // 透過 API 進行身份驗證，取得 token，JWT token 有效期限為 1 小時
            const response = await fetch("http://127.0.0.1:5000/api/login", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ username, password }),
            });
            const data = await response.json();

            // 模擬登入
            const users = JSON.parse(localStorage.getItem("users")) || [];
            const user = users.find(
              (user) =>
                user.username === username && user.plain_password === password
            );
            // let role = "user";

            if (user) {
              const token = "user-token";
              const userId = user.ID;
              const unitName = user.unit_name || "Default Unit"; // 使用者的單位名稱
              const role = "user";
              localStorage.setItem(
                "shopee:auth.state",
                JSON.stringify({ 
                  token, 
                  userId, 
                  unitName, 
                  role })
              );
              setInAuthenticated(true); // 設定為已登入
              setUserId(userId); // 設定使用者 ID
              setUnitName(unitName); // 設定單位名稱
              setRole(role); // 設定使用者角色
              return { token }; // 回傳 token
            // } else if (username === "admin" && password === "123456") {
            //   role = "admin";
            //   // 如果是系統管理員
            //   localStorage.setItem(
            //     "shopee:auth.state",
            //     JSON.stringify({
            //       token: "admin-token",
            //       userId: 0,
            //       unitName: "Admin Unit",
            //       role,
            //     })
            //   );
            //   setInAuthenticated(true);
            //   setUserId(0);
            //   setUnitName("Admin Unit");
            //   setRole(role);
            //   return { token: "admin-token" };
            // } else if (username === "user" && password === "123456") {
            //   role = "user";
            //   // 如果是一般使用者
            //   localStorage.setItem(
            //     "shopee:auth.state",
            //     JSON.stringify({
            //       token: "user-token",
            //       userId: 1,
            //       unitName: "User Unit",
            //       role,
            //     })
            //   );
            //   setInAuthenticated(true);
            //   setUserId(1);
            //   setUnitName("User Unit");
            //   setRole(role);
            //   return { token: "user-token" };
            } else if (data.token) {
              const decoded = jwtDecode(data.token);
              const unitName = decoded.unit_name || "Default Unit"; // 使用者的單位名稱
              localStorage.setItem(
                "shopee:auth.state",
                JSON.stringify({
                  token: data.token,
                  userId: decoded.userId,
                  unitName,
                  role: decoded.role,
                })
              );
              setInAuthenticated(true); // 設定為已登入
              setUserId(decoded.userId); // 設定使用者 ID
              setUnitName(unitName); // 設定單位名稱
              setRole(decoded.role); // 設定使用者角色
              return { token: data.token }; // 回傳 token
            } else {
              return { token: null, error: "帳號或密碼錯誤" };
            }
          } catch (error) {
            console.error("Login failed", error);
            return { token: null, error: "登入失敗，請稍後再試" };
          }
        },
        // 登出方法，清除登入狀態
        logout: async () => {
          setInAuthenticated(false);
          setUserId(null);
          setUnitName("");
          setRole("guest");
          localStorage.removeItem("shopee:auth.state");
          localStorage.removeItem("shopee:auth.token");
        },
        filterDataByRole,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
