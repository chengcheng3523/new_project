// React：使用 useState、createContext 和 useEffect 來管理狀態和建立 Context
// jwtDecode：用來解析 JWT（JSON Web Token），獲取使用者資訊
import React, { useState, createContext, useEffect } from "react";
import { jwtDecode } from 'jwt-decode';

// 設定初始的Context的預設值，在使用者未登入時適用
const defaultContextValue = {
  isAuthenticated: false, // 預設為未登入
  userId: null, // 預設沒有使用者 ID
  unitName: "", // 預設沒有單位名稱
  role: "guest", // 預設角色為訪客
};
// 創建 AuthContext 來提供全域的認證狀態
const AuthContext = createContext(defaultContextValue);

// 建立 AuthProvider 來管理認證狀態， Context 的提供者，讓整個應用程式的組件都能使用它
export const AuthProvider = ({ children }) => {
   // isAuthenticated 儲存使用者是否已登入，預設為 false
  const [isAuthenticated, setInAuthenticated] = useState(defaultContextValue.isAuthenticated);
  // userId 儲存使用者 ID，預設為 null
  const [userId, setUserId] = useState(defaultContextValue.userId);
  // unitName 儲存使用者單位名稱，預設為空字串
  const [unitName, setUnitName] = useState(defaultContextValue.unitName);
  // role 儲存使用者角色，預設為 "guest"
  const [role, setRole] = useState(defaultContextValue.role);
  

  
  // 檢查 LocalStorage 以恢復登入狀態
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
        const decoded = jwtDecode(token);
        setInAuthenticated(true);
        setUserId(decoded.sub.userId);
        setUnitName(decoded.sub.unitName);
        const roleFromToken = decoded.sub.role || "user";
        setRole(roleFromToken);
        console.log("目前的角色:", roleFromToken);
      } else {
        // 如果都沒有，確保設置為未登入
        setInAuthenticated(false);
      }
    } catch (error) {
      console.error("Failed to parse auth state from localStorage", error);
      // 在錯誤時也可以考慮清除 localStorage 的相關資訊
    }
  }, []);

  // 定義依角色過濾資料的方法
  // admin 看到所有資料，一般使用者只能看到自己的資料
  const filterDataByRole = (data) => {
    return role === "admin"
      ? data
      : data.filter((item) => item.user_id === userId);
  };

    return (
      // 將 AuthContext 內的值提供給子組件
      // 透過 AuthContext.Provider 提供 isAuthenticated、userId、role 等狀態，讓其他組件能使用。
      <AuthContext.Provider
      value={{
        isAuthenticated,
        userId,
        unitName,
        role,

        // 提供登入方法，檢查使用者是否輸入帳號和密碼
        login: async (username, password) => {
          if (!username || !password) {
            return { token: null, error: "請輸入帳號和密碼" };
          }
          try {
            const response = await fetch("http://127.0.0.1:5000/api/login", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (data.token) {
              const decoded = jwtDecode(data.token);
              console.log("登入成功,解析Decoded JWT:", decoded);
              console.log("Unit Name:", decoded.sub.unitName);
              console.log("解析出的角色:", decoded.sub?.role || decoded.role);
              console.log("從 localStorage 恢復的角色:", decoded.role);
              console.log("目前的角色狀態:", role);

              localStorage.setItem(
                "shopee:auth.state",
                JSON.stringify({
                  token: data.token,
                  userId: decoded.sub.userId,
                  unitName: decoded.sub.unitName, 
                  role: decoded.sub.role,
                })
              );

              setInAuthenticated(true);
              setUserId(decoded.sub.userId);
              setRole(decoded.sub.role); // 更新角色狀態為從 token 獲取的角色
              setUnitName(decoded.sub.unitName); 
              return { token: data.token };
              
            } else if (username === "admin" && password === "123456") {
              const role = "admin"; // 使用 let 來定義 role
              // 如果是系統管理員
              localStorage.setItem(
                "shopee:auth.state",
                JSON.stringify({
                  token: "admin-token",
                  userId: 1,
                  unitName: "Admin Unit",
                  role,
                })
              );
              setInAuthenticated(true);
              setUserId(1);
              setUnitName("Admin Unit");
              setRole(role);
              return { token: "admin-token" };

            } else {
              return { token: null, error: "帳號或密碼錯誤" };
            }
          } catch (error) {
            console.error("Login failed", error);
            return { token: null, error: "登入失敗，請稍後再試" };
          }
        },
        // 提供登出方法
        // 登出時，將 isAuthenticated 設為 false，清空 userId、unitName 和 role
        logout: async () => {
          setInAuthenticated(false);
          setUserId(null);
          setUnitName("");
          setRole("guest");
          // 移除 localStorage 中的登入資訊
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

export default AuthContext;// 匯出 AuthContext，供其他組件使用。
