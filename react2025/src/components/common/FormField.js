import React from 'react';
import Label from './Label';
import Input from './Input';

const FormField = ({ id, name, type, value, onChange, label, required }) => (
  <div className="mb-3">
    <Label htmlFor={id}>
      {label} {required && <span style={{ color: 'red' }}>*</span>}
    </Label>
    <Input
      type={type}
      id={id}
      name={name}
      value={value}
      required={required}
      onChange={onChange}
    />
  </div>
);

export default FormField;