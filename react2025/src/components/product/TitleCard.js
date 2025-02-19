import React from 'react';
import styled from 'styled-components';
import 'bootstrap/dist/css/bootstrap.min.css';

// Card 元件，用於顯示卡片
const Card = styled.div`
    border: 1px solid #e8e8e8; // 卡片邊框顏色
    border-radius: 4px; // 卡片邊框圓角
    overflow: hidden; // 隱藏超出卡片範圍的內容
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); // 卡片陰影
    transition: box-shadow 0.3s;// 卡片陰影過渡效果
    &:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.7); // 懸停時的卡片陰影
    }
    padding: 16px; // 卡片內邊距
    margin: 16px; // 卡片外邊距
`;

// CardTitle 元件，用於顯示卡片標題
const CardTitle = styled.h3`
    margin: 0 0 16px 0; // 卡片標題的外邊距
    font-size: 1.25em; // 卡片標題的字體大小
`;

// TitleCard 元件，用於顯示產品卡片
const TitleCard = ({
    title,
}) => {
    return (
        <Card className="card">
            <CardTitle className="card-title">{title}</CardTitle>
        </Card>
    );
};

export default TitleCard; // 匯出 TitleCard 元件