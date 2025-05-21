import styled from 'styled-components';

const Form = styled.form`
  max-width: 600px;
  margin: auto;
  padding: 24px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  
  h4 {
    margin-bottom: 16px;
    font-size: 1.5em;
    color: #333;
  }

  .mb-3 {
    margin-bottom: 16px;
  }

  label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #555;
  }

  input {
    padding: 10px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
    &:focus {
      border-color: #80bdff;
      outline: 0;
      box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }
  }

  button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    font-size: 1em;
    cursor: pointer;
    &:hover {
      background-color: #0056b3;
    }
  }
`;

export default Form;