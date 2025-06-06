import React from 'react';
import styled, { css } from 'styled-components';
import Header from './Header';
import Footer from './Footer';
import Container from '../common/Container';
const PageHeader = styled(Header)`
  ${(props) =>
    props.fixed &&
    css`
      z-index: 1;
      position: fixed;
    `}
`;

const DefaultLayout = ({ fixedHeader, children }) => {
  return (
    <div>
      <PageHeader fixed={fixedHeader} />
      {/* Add other components here */}
      <Container>{children}</Container>
      {/* Add other components here */}
      <Footer />
      {/* Add other components here */}
    </div>
  );
};

export default DefaultLayout;