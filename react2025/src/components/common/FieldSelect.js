import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  font-size: 1rem;
  color: #333;
`;

const Required = styled.span`
  color: red;
`;

const Select = styled.select`
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

const FieldSelect = ({ id, name, value, onChange, label, required, children }) => {
  return (
    <Container>
      <Label htmlFor={id}>
        {label} {required && <Required>*</Required>}
      </Label>
      <Select id={id} name={name} value={value} onChange={onChange} required={required}>
        {children}
      </Select>
    </Container>
  );
};

export default FieldSelect;