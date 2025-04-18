// 一個單選的下拉選單
import React from 'react';
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

const MultiSelectField = ({ id, name, value, onChange, label, required, options }) => {
  return (
    <Container>
      <StyledLabel htmlFor={id}>
        {label} {required && <Required>*</Required>}
      </StyledLabel>
      <Select
        id={id}
        name={name}
        value={value}
        required={required}
        onChange={onChange}
      >
        {options && options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </Select>
    </Container>
  );
};

export default MultiSelectField;