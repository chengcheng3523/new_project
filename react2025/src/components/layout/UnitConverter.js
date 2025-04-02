import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  flex: 1 1 400px;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
`;

const Section = styled.div`
  flex: 1 1 400px;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
`;


const Select = styled.select`
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
`;

const Title = styled.h2`
  margin-top: 0;
`;

const DisplayInput = styled.input`
  width: 220px;
  font-size: 18px;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
`;

const ButtonGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 50px);
  gap: 10px;
  margin-top: 10px;
`;

const Button = styled.button`
  font-size: 18px;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
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

  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
    <label>
      輸入數值：
      <input
        type="number"
        value={unitInput}
        onChange={(e) => setUnitInput(e.target.value)}
        placeholder="請輸入數值"
        style={{
          width: '15%',
          padding: '8px',
          borderRadius: '5px',
          border: '1px solid #ccc'
        }}
      />
    </label>

    <label>
      單位類別：
      <Select
        value={unitType}
        onChange={(e) => setUnitType(e.target.value)}
        style={{width: '15%', padding: '8px', borderRadius: '5px', border: '1px solid #ccc' }}
      >
        <option value="length">長度</option>
        <option value="weight">重量</option>
        <option value="temperature">溫度</option>
        <option value="area">面積</option>
        <option value="CC">容積</option>
      </Select>
    </label>

      <label style={{ flex: 1 }}>
        從：
        <select
          value={fromUnit}
          onChange={(e) => setFromUnit(e.target.value)}
          style={{ width: '20%', padding: '8px', borderRadius: '5px', border: '1px solid #ccc' }}
        >
          {unitOptions[unitType].map((unit) => (
            <option key={unit} value={unit}>{unit}</option>
          ))}
        </select>
      </label>

      <label style={{ flex: 1 }}>
        到：
        <select
          value={toUnit}
          onChange={(e) => setToUnit(e.target.value)}
          style={{ width: '20%', padding: '8px', borderRadius: '5px', border: '1px solid #ccc' }}
        >
          {unitOptions[unitType].map((unit) => (
            <option key={unit} value={unit}>{unit}</option>
          ))}
        </select>
      </label>


    <button
      onClick={convertUnit}
      style={{
        width: '20%',
        padding: '10px',
        background: '#4CAF50',
        color: '#fff',
        border: 'none',
        borderRadius: '6px',
        fontWeight: 'bold',
        cursor: 'pointer'
      }}
    >
      換算
    </button>

    <p style={{ fontWeight: 'bold', marginTop: '10px' }}>{unitResult}</p>
  </div>
</Section>

    </Container>
  );
};

export default UnitConverter;
