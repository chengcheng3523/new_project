import React from 'react';
import Label from './Label';
import Input from './Input';

const FormField = ({ id, name, type, value, onChange, label, required, readOnly }) => (
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
      readOnly={readOnly} // ✅ 確保 readOnly 正確傳遞
    />
  </div>
);

export default FormField;