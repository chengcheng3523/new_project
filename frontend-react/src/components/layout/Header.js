import React ,{ useContext }from "react";
import styled from "styled-components";
import Container from "../common/Container";
import Logo from "../images/logo.png";
// import { Input } from "antd"; 
// import { ShoppingCartOutlined  } from "@ant-design/icons"; 
import { Link } from "react-router-dom";
import AuthContext from "../auth/AuthContext";

// const StyledHeader = styled.header`
//   background-color: #d1011c;
//   width: 100vw;
//   padding: 10px ;
// `;
const StyledHeader = styled.header`
  background-color: #75aee4;
  width: 100vw;
  padding: 10px ;
`;
const StyledHeaderSection = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px
 `;

const Navigetor = styled.div`
a{
  margin:0px 4px;
  color: white;
  text-decoration: none;
}
`;

const Toolbar = styled.div`
a{
  margin:0px 10px;
  color: white;
  text-decoration: none;
}
`;
const Box = styled.div`
  display: flex;
  align-items: center;
  padding: 0px 10px;
`;

// const Logo = styled

const Header = (className) => {
  const{isAuthenticated, unitName, logout} =useContext(AuthContext);
  console.log("AuthContext 数据:", { isAuthenticated, unitName });
  console.log("localStorage 数据:", localStorage.getItem("shopee:auth.state"));
  console.log("isAuthenticated:", isAuthenticated);
  console.log("logout:", logout);
  console.log("unitName:", unitName);
  return (
    <StyledHeader className={className}>
      <Container> 
        <StyledHeaderSection>
          <Navigetor>
            <Link to="/mall">首頁</Link>
          </Navigetor>
          <Toolbar>
            {/* <a href="#!">通知</a> */}
            {/* <a href="#!">幫助中心</a> */}
            {/* <a href="#!">登入/註冊</a>*/}
            {isAuthenticated ? (
              <div style={{ display: "flex", alignItems: "center" }}>
                <a href="#!" style={{ marginRight: 8 }}>{unitName}</a> {/* 将单位名称放在登出按钮左侧 */}
                <span>|</span>
                <span onClick={() => {
                    logout();
                    console.log("unitName:", unitName);
                    window.location.reload(); // 重载页面以更新状态
                }}
                style={{ marginLeft: 8, cursor: "pointer" }} // 添加 cursor 样式以指示可点击
              >登出</span>
              </div>
            ) : (
              <Link to="/login">登入/註冊</Link>
            )}
          </Toolbar>
        </StyledHeaderSection>  
        <StyledHeaderSection>
          <Link to="/mall">
            <img src={Logo} alt="logo" height={33}></img> {/* <Logo/> */}
          </Link>
          <Box>
            {/* <span>Search</span> */}


          </Box>
        </StyledHeaderSection>
      </Container> {/* RWD */}
    </StyledHeader>
  );
};

export default Header;