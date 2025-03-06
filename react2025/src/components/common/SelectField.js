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

const SelectField = ({ id, name, value = [], onChange, label, required, options, inputOption }) => {
  const [selectedValues, setSelectedValues] = useState(Array.isArray(value) ? value : [value]);
  const [showInput, setShowInput] = useState(false);
  const [inputValue, setInputValue] = useState('');

  useEffect(() => {
    setShowInput(selectedValues.includes(inputOption));
  }, [selectedValues, inputOption]);

  const handleSelectChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions, (option) => option.value);
    setSelectedValues(selectedOptions);
    onChange({ target: { name, value: selectedOptions } });
  };

  const handleInputChange = (e) => {
    const newValue = e.target.value;
    setInputValue(newValue);
    onChange({
      target: { name, value: selectedValues.includes(inputOption) ? [...selectedValues.filter(v => v !== inputOption), `${inputOption}${newValue}`] : selectedValues }
    });
  };

  return (
    <Container>
      <StyledLabel htmlFor={id}>
        {label} {required && <Required>*</Required>}
      </StyledLabel>
      <Select
        id={id}
        name={name}
        multiple // 允许多选
        value={selectedValues}
        required={required}
        onChange={handleSelectChange}
      >
        {options && options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </Select>
      {showInput && (
        <Input
          type="text"
          placeholder="請填寫"
          value={inputValue}
          onChange={handleInputChange}
        />
      )}
    </Container>
  );
};

export default SelectField;
