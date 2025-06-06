// import { PropertySafetyFilled } from '@ant-design/icons';
// import React from 'react';
import styled from 'styled-components';

const Image = styled.div`
  width: 100%;
  height: ${(props) => props.height}px;
  background-image: ${(props) => `url(${props.url})`};
  background-position: center;
  background-size: cover;
`;

export default Image;