// // 資料顯示與操作元件，根據角色控制權限
// import React, { useContext } from 'react';
// import AuthContext from '../auth/AuthContext';

// const DataManagement = () => {
//   const { isAuthenticated, role } = useContext(AuthContext);

//   return (
//     <div>
//       <h2>資料管理系統</h2>
//       {isAuthenticated ? (
//         role === 'admin' ? (
//           <>
//             <button>新增資料</button>
//             <button>修改資料</button>
//             <button>刪除資料</button>
            
//           </>
//         ) : (
//           <button disabled>僅可輸入資料（不可修改）</button>
//         )
//       ) : (
//         <p>未登入僅可查看資料</p>
//       )}
//     </div>
//   );
// };

// export default DataManagement; // 匯出資料管理元件