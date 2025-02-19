import styled from 'styled-components';

const Button = styled.button`
  padding: 8px 16px;
  border: 2px solid goldenrod;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  font-size: 1em;
  margin: 2px; /* 增加按鈕之間的間距 */
  cursor: pointer;
  &:hover {
    background-color: #0056b3;
  }
`;

const DeleteButton = styled(Button)`

  margin: 2px; /* 增加按鈕之間的間距 */
  padding: 8px 16px;
  border: 2px solid goldenrod;
  border-radius: 4px;
  background-color: #dc3545;
  color: white;
  font-size: 1em;
  cursor: pointer;
  &:hover {
    background-color: #c82333;
  }
`;

const EditButton = styled(Button)`

  margin: 2px; /* 增加按鈕之間的間距 */
  padding: 8px 16px;
  border: 2px solid goldenrod;
  font-size: 1em;
  background-color: #ffc107;
  &:hover {
    background-color:rgb(201, 201, 191);
  }
`;

export { Button, DeleteButton, EditButton };