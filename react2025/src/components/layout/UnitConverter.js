import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  display: flex; /* 水平排列 */
  flex-direction: row;
  gap: 30px; /* 增加左右區塊的間距 */
  padding: 30px; /* 增加內部間距 */
  margin: 20px auto; /* 讓容器與外部內容保持距離 */
  background: #f9f9f9; /* 改變背景顏色 */
  border-radius: 15px; /* 圓角 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15); /* 增加陰影效果 */
  
  /* 當螢幕寬度小於768px時，改為垂直排列 */
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 20px; /* 調整垂直間距 */
  }
`;

const Section = styled.div`
  flex: 1; /* 讓兩個區塊平分空間 */
  background: white;
  padding: 20px;/* 增加內部間距 */
  border-radius: 10px; /* 圓角 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);/* 調整陰影 */
  border: 1px solid #ddd; /* 增加邊框 */
`;


const Select = styled.select`
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
`;

const Title = styled.h2`
  margin-top: 0;
  margin-bottom: 20px; /* 增加標題與內容的距離 */
  font-size: 24px; /* 調整字體大小 */
  color: #333; /* 改變字體顏色 */
  text-align: center; /* 置中標題 */
`;

const DisplayInput = styled.input`
  width: 100%; /* 占滿區塊寬度 */
  font-size: 18px;
  padding: 12px; /* 增加內部間距 */
  margin: 10px 0; /* 增加上下間距 */
  border: 1px solid #ccc;
  border-radius: 8px; /* 圓角 */
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1); /* 增加內陰影 */
`;

const ButtonGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 50px);
  gap: 10px;
  margin-top: 10px;

  /* 置中 ButtonGrid */
  justify-content: center; /* 水平置中 */
  align-items: center; /* 垂直置中 */
`;

const Button = styled.button`
  font-size: 18px; /* 調整字體大小 */
  padding: 12px;/* 增加按鈕內部間距 */
  margin: 5px 0;/* 增加按鈕之間的間距 */
  border: 1px solid #ccc;
  border-radius: 8px; /* 圓角 */
  background-color: #f0f0f0; /* 按鈕背景色 */
  cursor: pointer;

  &:hover {
    background-color: #e0e0e0; /* 滑鼠懸停效果 */
  }
`;

// 這裡是單位換算的容器
const UnitConverterContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px; /* 增加項目之間的間距 */
  padding: 20px;
  background: #f9f9f9; /* 背景顏色 */
  border-radius: 10px; /* 圓角 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 陰影效果 */
`;

const Label = styled.label`
  display: flex;
  flex-direction: column;
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-top: 5px;
`;

const ConvertButton = styled.button`
  width: 100%;
  padding: 12px;
  background: #4caf50;
  color: white;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;

  &:hover {
    background: #45a049; /* 滑鼠懸停效果 */
  }
`;

const ResultText = styled.p`
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-top: 10px;
  text-align: center;
`;



const unitOptions = {
  length: ['公尺', '公里', '公分', '英吋', '英尺'],
  weight: ['公斤', '克', '磅', '公噸', '台斤', '毫克'],
  area: ['平方公尺', '平方公里', '英畝', '公畝', '公頃', '甲', '坪'],
  temperature: ['攝氏', '華氏', '開爾文'],
  CC: ['公升', '毫升']
};



const UnitConverter = () => {
  const [calcDisplay, setCalcDisplay] = useState('');
  const [unitType, setUnitType] = useState('length');
  const [fromUnit, setFromUnit] = useState('公尺');
  const [toUnit, setToUnit] = useState('公尺');
  const [unitInput, setUnitInput] = useState('');
  const [unitResult, setUnitResult] = useState('');

  useEffect(() => {
    setFromUnit(unitOptions[unitType][0]);
    setToUnit(unitOptions[unitType][0]);
  }, [unitType]);

  const press = (val) => {
    setCalcDisplay((prev) => prev + val);
  };

  const clearDisplay = () => {
    setCalcDisplay('');
  };

  const calculate = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/calc', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression: calcDisplay })
      });

      const data = await res.json();

      if (res.ok) {
        setCalcDisplay(data.result ?? '錯誤');
      } else {
        setCalcDisplay('錯誤的運算式');
      }
    } catch (error) {
      setCalcDisplay('錯誤');
    }
  };

  const convertUnit = async () => {
    try {
      if (!fromUnit || !toUnit) {
        setUnitResult('請選擇要轉換的單位');
        return;
      }

      const res = await fetch('http://localhost:5000/api/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          value: unitInput,
          from: fromUnit,
          to: toUnit,
          type: unitType
        })
      });

      const data = await res.json();

      if (res.ok) {
        setUnitResult(data.error ? `錯誤：${data.error}` : `${unitInput} ${fromUnit} = ${data.result} ${toUnit}`);
      } else {
        setUnitResult('無法換算，請確認輸入與單位');
      }
    } catch (error) {
      setUnitResult('換算錯誤，請稍後再試');
    }
  };

  return (
    <Container>
      <Section>
        <Title>基本計算機</Title>
        <DisplayInput type="text" value={calcDisplay} readOnly />
        <ButtonGrid>
          <Button onClick={() => press('7')}>7</Button>
          <Button onClick={() => press('8')}>8</Button>
          <Button onClick={() => press('9')}>9</Button>
          <Button onClick={() => press('/')}>÷</Button>
          <Button onClick={() => press('4')}>4</Button>
          <Button onClick={() => press('5')}>5</Button>
          <Button onClick={() => press('6')}>6</Button>
          <Button onClick={() => press('*')}>×</Button>
          <Button onClick={() => press('1')}>1</Button>
          <Button onClick={() => press('2')}>2</Button>
          <Button onClick={() => press('3')}>3</Button>
          <Button onClick={() => press('-')}>−</Button>
          <Button onClick={() => press('0')}>0</Button>
          <Button onClick={() => press('.')}>.</Button>
          <Button onClick={calculate}>=</Button>
          <Button onClick={() => press('+')}>+</Button>
          <Button onClick={clearDisplay} style={{ gridColumn: 'span 4', background: '#fdd' }}>清除</Button>
        </ButtonGrid>
      </Section>
      
      <Section>
        <Title>單位換算</Title>
        <UnitConverterContainer>
          <Label>
            輸入數值：
            <Input
              type="number"
              value={unitInput}
              onChange={(e) => setUnitInput(e.target.value)}
              placeholder="請輸入數值"
            />
          </Label>

          <Label>
            單位類別：
            <Select
              value={unitType}
              onChange={(e) => setUnitType(e.target.value)}
            >
              <option value="length">長度</option>
              <option value="weight">重量</option>
              <option value="temperature">溫度</option>
              <option value="area">面積</option>
              <option value="CC">容積</option>
            </Select>
          </Label>

          <Label>
            從：
            <Select
              value={fromUnit}
              onChange={(e) => setFromUnit(e.target.value)}
            >
              {unitOptions[unitType].map((unit) => (
                <option key={unit} value={unit}>{unit}</option>
              ))}
            </Select>
          </Label>

          <Label>
            到：
            <Select
              value={toUnit}
              onChange={(e) => setToUnit(e.target.value)}
            >
              {unitOptions[unitType].map((unit) => (
                <option key={unit} value={unit}>{unit}</option>
              ))}
            </Select>
          </Label>

          <ConvertButton onClick={convertUnit}>換算</ConvertButton>
          <ResultText>{unitResult}</ResultText>
        </UnitConverterContainer>
      </Section>

    </Container>
  );
};

export default UnitConverter;
