import React from'react';
import DefaultLayout from '../components/layout/DefaultLayout';
import styled from 'styled-components';
import Container from '../components/common/Container';
import LoginForm from '../components/auth/LoginForm'; // 確保路徑正確

const StyledLoginBox =styled.div`
  background-color: white;
`;

const StyledLoginContainer =styled(Container)`
  display: flex;
  justify-content: space-between;
  padding: 48px 0;
`;


const LoginPage = () => {
  return (
    <DefaultLayout> 
      <StyledLoginBox>
        <StyledLoginContainer>
          {/* <div>
            <img
              width="100"
              src="https://img-baofun.zhhainiao.com/pcwallpaper_ugc_mobile/static/05b9f74849526126fdf856053444a654.png?x-oss-process=image%2Fresize%2Cm_lfit%2Cw_640%2Ch_1138"
              alt=""
            />
            </div> */}
          <LoginForm/>
        </StyledLoginContainer>
      </StyledLoginBox> 
    </DefaultLayout>
  );
};

export default LoginPage;