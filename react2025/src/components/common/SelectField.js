// 一個單選的下拉選單並且支持一個(其他)選項
import React, { useState, useEffect } from 'react';
import Label from './Label';
import styled from "styled-components";

// Styled-components
const Container = styled.div`
  margin-bottom: 20px; /* 下拉框容器的底部间距 */
`;

const StyledLabel = styled(Label)`
  font-size: 1rem;
  color: #333;
`;

const Required = styled.span`
  color: red;
`;

const Select = styled.select`
  width: 100%; /* 下拉框宽度占满容器 */
  padding: 10px;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  background-color: #fff;
  transition: border 0.3s ease;

  &:focus {
    border-color: #007bff; /* 聚焦时的边框颜色 */
    outline: none;
  }
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  background-color: #fff;
  transition: border 0.3s ease;

  &:focus {
    border-color: #007bff;
    outline: none;
  }
`;

const SelectField = ({ id, name, value = '', onChange, label, required, options, inputOption }) => {

  const [selectedValue, setSelectedValue] = useState(value || '');
  const [showInput, setShowInput] = useState(false);
  const [inputValue, setInputValue] = useState('');

  // 修改：根據 value 初始化 showInput 和 inputValue
  useEffect(() => {
    const isOther = value && !options.some(opt => opt.value === value); // 檢查 value 是否不在預設選項中
    setSelectedValue(isOther ? inputOption : value); // 如果是「其他」，設為 inputOption
    setShowInput(isOther && inputOption === value);  // 如果選擇「其他」，顯示輸入框
    setInputValue(isOther ? value : '');             // 如果是「其他」，提取自訂值
  }, [value, inputOption, options]);

  // 修改：處理單選邏輯，並在選擇「其他」時顯示輸入框
  const handleSelectChange = (e) => {
    const newValue = e.target.value;
    setSelectedValue(newValue);
    setShowInput(newValue === inputOption); // 當選擇「其他」時顯示輸入框
    if (newValue !== inputOption) {
      onChange({ target: { name, value: newValue } }); // 直接傳遞選擇的值
    }
  };

  // 修改：處理「其他」選項的自訂輸入，並將最終值傳回父組件
  const handleInputChange = (e) => {
    const newInput = e.target.value;
    setInputValue(newInput);
    onChange({ target: { name, value: newInput } }); // 傳遞自訂值
  };
 
  
  return (
    <Container>
      <StyledLabel htmlFor={id}>
        {label} {required && <Required>*</Required>}
      </StyledLabel> 
      <Select
        id={id}
        name={name}
        value={selectedValue}
        required={required}
        onChange={handleSelectChange}
      >
        <option value="">請選擇</option> 
        {options && options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </Select> 
      {showInput && (
        <Input
          type="text"
          placeholder="請填寫其他單位"
          value={inputValue}
          onChange={handleInputChange}
          required  
        />
      )}
    </Container>
  );
};

export default SelectField;
