import React ,{ useContext }from "react";
import styled from "styled-components";
import Container from "../common/Container";
import Logo from "../images/logo.png";
import { Input } from "antd"; // 導入 Input 元素
import { ShoppingCartOutlined  } from "@ant-design/icons"; // 從 @ant-design/icons 導入 ShoppingCartOutlined
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
  return (
    <StyledHeader className={className}>
      <Container> 
        <StyledHeaderSection>
          <Navigetor>
            <a href="#!">購物</a>
            <a href="#!">下載</a>
            <a href="#!">追蹤我們</a>
            <a href="#!">部落格</a>
          </Navigetor>
          <Toolbar>
            <a href="#!">通知</a>
            <a href="#!">幫助中心</a>
            {/* <a href="#!">登入/註冊</a>*/}
            {isAuthenticated ? (
              <div>
                <a href="#!">{unitName}</a>
                <span>|</span>
                <span onClick={() => {
                  logout();
                  console.log("unitName:", unitName);
                  window.location.reload(); // 重载页面以更新状态
                }}>登出</span>
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
            <Input.Search
              style={{ marginRight: 8 }}
              placeholder="搜尋"
              omSearch={(value) => console.log(value)}
              enterButton
            />
            <Link to="/cart">
              <ShoppingCartOutlined style={{ fontSize: 28, color: "white" }} />
            </Link>
          </Box>
        </StyledHeaderSection>
      </Container> {/* RWD */}
    </StyledHeader>
  );
};

export default Header;