import React from "react";
import styled from "styled-components";
import Container from "../common/Container";
import { Link } from "react-router-dom";
import CVSLogo from "../images/CVSLogo.png";
import Remark from "../images/Remark.png";
import QRCode from "../images/QRCode.png";

const StyledFooter = styled.footer `
    background-color: #fbfbfb;
    padding: 20px 0px;
    padding-top: 40px 0px;
    padding-bottom: 40px 0px;
`;

const FooterColumn = styled.div`
    display: flex;
    flex-direction: column;
    margin-bottom:16px;
    width: 33.33%;
    @media (min-width: 769px) {
        width:20%;
    }
    a{
    color:rgba(0,0,0,0.54);
    margin-bottom: 2px;
    text-decoration: none;
    }
`;

const FooterColumnTitle = styled.h4`
    font-weight: bold;
    margin-bottom: 12px;
`;

const Box = styled.div`
    display: flex;
    Flex-wrap: wrap;
`;

const Footer = ()=> {
    return <StyledFooter>
        <Container>
        <Box>
            <FooterColumn>
                <FooterColumnTitle>客服中心</FooterColumnTitle>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
            </FooterColumn>
            <FooterColumn>
                <FooterColumnTitle>關於</FooterColumnTitle>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
            </FooterColumn>
            <FooterColumn>
                <FooterColumnTitle>物流合作</FooterColumnTitle>
                <img 
                    src={CVSLogo} 
                    alt="CVSLogo" 
                    width="30px" 
                    style={{ marginBottom:12 }}
                />
                  <FooterColumnTitle>24小時包裝減量標章</FooterColumnTitle>
                  <img 
                    src={Remark} 
                    alt="CVSLogo" 
                    width="30px" 
                    style={{ marginBottom:12 }}
                />
            </FooterColumn>
            <FooterColumn>
                <FooterColumnTitle>關注我們</FooterColumnTitle>
                <Link to="#!">FB</Link>
                <Link to="#!">IG</Link>
                <Link to="#!">LINE</Link>
                <Link to="#!">Blog</Link>
                <Link to="#!">in</Link>
                <Link to="#!">幫助中心</Link>
                <Link to="#!">幫助中心</Link>
            </FooterColumn>
            <FooterColumn>
            <FooterColumnTitle>下載</FooterColumnTitle>
                <Box>
                    <img 
                    src={QRCode} 
                    alt="QRCode" 
                    width="30%" 
                    style={{ marginBottom:12 }}
                    />
                    <div>
                    <div>AppStore</div>
                    <div>GooglePlat</div>
                    </div>
                </Box>
            </FooterColumn>
        </Box>
        </Container>
        </StyledFooter>;
};

export default Footer;