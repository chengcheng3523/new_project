import React from "react";
import styled from "styled-components";
import Container from "../common/Container";
import { Link } from "react-router-dom";
// import CVSLogo from "../images/CVSLogo.png";
// import Remark from "../images/Remark.png";
// import QRCode from "../images/QRCode.png";

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
                <FooterColumnTitle>聯絡我們</FooterColumnTitle>
                <Link to="#!">地址:333桃園市龜山區萬壽路一段300號</Link>
            </FooterColumn>
            <FooterColumn>
                <FooterColumnTitle>連絡電話</FooterColumnTitle>
                <Link to="#!">0912345678</Link>
            </FooterColumn>
            <FooterColumn>
                <FooterColumnTitle>專題題目</FooterColumnTitle>
                <Link to="#!">農業溯源系統</Link>
            </FooterColumn>
            <FooterColumn>
                <FooterColumnTitle>成員</FooterColumnTitle>
                <Link to="#!">謝益仁</Link>
                <Link to="#!">陳吟甄</Link>
                {/* <Link to="#!">LINE</Link> */}
                {/* <Link to="#!"></Link>
                <Link to="#!"></Link> */}
            </FooterColumn>
        </Box>
        </Container>
        </StyledFooter>;
};

export default Footer;