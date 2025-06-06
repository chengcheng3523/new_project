import React, { useState } from 'react';
import { Modal } from 'antd';
import { Link } from 'react-router-dom';
import { useEffect } from 'react';
const eventProductId = 'p003';

const PopupModal = () => {
  const [isVisble, setIsVisble] = useState(true);

  useEffect(() => {
    const popupHistory = JSON.parse(
        localStorage.getItem("popup:popup.history")
    );
    if (popupHistory && Date.now() - popupHistory.time < 3 * 1000) {// console.log(Date.now(), popupHistory.time,Date.now() - popupHistory.time);
      setIsVisble(false);
    } else {
      const history = {
          time: Date.now(),
          productId: eventProductId,
      };
      localStorage.setItem("popup:popup.history",JSON.stringify(history));
    }
  }, []);

  return (
    isVisble && (
      <Modal 
        // title="Basic Modal" 
        visible
        footer={null}
        onOk={() => setIsVisble(false)}  
        onCancel={() => setIsVisble(false)}  
      >
        <Link to={`/${eventProductId}`}>
          <img 
          alt={`/${eventProductId}-event`} 
          // src='https://images.unsplash.com/photo-1729731322011-f945437445be?q=80&w=1287&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D' 
          />
        </Link>
      </Modal>
    )
  );
};

export default PopupModal;