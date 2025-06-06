import { useEffect } from "react";
import { useLocation } from "react-router-dom";

//export default function ScrollToTop() { //建立一個functionc或
const ScrollToTop = () => {  //建立一個const
  const { pathname } = useLocation();   //若pathname有變動，Location=URL拿到pathname

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);   
  //判斷pathname是否有變動，若有變動則執行 window.scrollTo(0, 0)
  //scrollTo第一個是X軸左右，切到最左邊，第二個是Y軸，切到最上面
  //如果URL沒有變化，就不會執行這個useEffect

  return null;  //不用return任何東西
}

export default ScrollToTop;  //使用 const 加上 export default ScrollToTop; 來導出