import React, { useState , useEffect , useContext, useCallback  } from 'react';
import Clearfix from "../components/common/Clearfix";
// import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import moment from 'moment';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';
import Mock from 'mockjs';

const Page01 = () => {
  const { role, filterDataByRole ,userId } = useContext(AuthContext); // 獲取使用者角色和過濾方法
  // const isAdmin = role === 'admin'; // 判斷是否為管理員
  const isAdmin = role?.toLowerCase() === "admin"; // 判斷是否為管理員
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, // 新增 user_id
    unit_name: '',
    farmer_name: '',
    phone: '',
    fax: '',
    mobile: '',
    address: '',
    email: '',
    total_area: '',
    notes: '',
    Number: '',
    LandParcelNumber: '',
    Area: '',
    Crop: '',
  });

  const [data, setData] = useState([]); // 保存數據到狀態，定義 value 狀態
  const [loading, setLoading] = useState(false); // 控制提交按鈕的加載狀態

  // 模擬獲取數據
  const fetchData = useCallback(async () => {
    try {
      const response = Mock.mock({
        'data|7': [
          [
            '@increment', // 自增 ID
            userId, // 使用者 ID
            '@word', // 單位名稱
            '@name', // 農戶姓名
            '@phone', // 電話
            '@phone', // 傳真
            '@phone', // 行動電話
            '@county(true)', // 地址
            '@EMAIL', // 電子郵件
            '@float(1, 100, 2, 2)', // 面積
            '@sentence(3, 5)', // 備註
            '@word', // 編號
            '@word', // 地籍號碼
            '@float(1, 100, 2, 2)', // 面積
            '@word', // 作物
          ],
        ],
      });
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id:  item[0],
          user_id: item[1],
          unit_name: item[2],
          farmer_name: item[3],
          phone: item[4],
          fax: item[5],
          mobile: item[6],
          address: item[7],
          email: item[8],
          total_area: item[9],
          notes: item[10],
          Number: item[11],
          LandParcelNumber: item[12],
          Area: item[13],
          Crop: item[14],
        }));
        const filteredData = filterDataByRole(transformedData);
        console.log('過濾後的數據:', filteredData); // 打印過濾後的數據
        setData(filteredData);
      } else {
        alert('伺服器返回錯誤，請稍後重試！');
      }
    } catch (error) {
      console.error('獲取數據失敗:', error);
      alert('無法載入數據，請檢查您的伺服器或網絡連接！');
    }
  }, [filterDataByRole, userId]);

  
  useEffect(() => {
    console.log('Data to be displayed:');
    console.log('Fetching data...');
    fetchData(); // 組件加載時獲取數據
  }, [fetchData]); // 這裡 fetchData 依賴於 useCallback

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // 阻止表單默認提交行為
    setLoading(true); // 開啟加載狀態
    try {
      // 格式化日期為 MySQL 支持的格式
      if (formData.OperationDate) {
        formData.OperationDate = moment(formData.OperationDate).format('YYYY-MM-DD HH:mm:ss');
      }
      // const response = await axios.post('http://localhost:5000/api/records03/post', formData);
      let response;
      if (formData.id) {
        // 更新現有資料
        response = {
          data: data.map(item => item.id === formData.id ? { ...formData, id: item.id } : item),
        };
      } else {
        // 新增資料
        response = {
          data: [
            ...data,
            {
              id: data.length + 1,
              ...formData,
            },
          ],
        };
      }
      setData(response.data); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId, // 新增 user_id
        unit_name: '',
        farmer_name: '',
        phone: '',
        fax: '',
        mobile: '',
        address: '',
        email: '',
        total_area: '',
        notes: '',
        Number: '',
        LandParcelNumber: '',
        Area: '',
        Crop: '',
      }); // 清空表單
      alert('成功儲存資料！'); // 成功提示
      console.log('成功發送請求，回應:', response.data);
    } catch (error) {
      console.error('發送請求失敗:', error);
      alert('儲存失敗，請稍後重試！'); // 錯誤提示
    } finally {
      setLoading(false); // 關閉加載狀態
    }
  };

  const handleDelete = async (id) => {
    if (!isAdmin) return; // 如果不是管理員，則返回
    try {
      // const response = await axios.delete(`http://localhost:5000/api/records03/delete/${id}`);
      // 模擬刪除數據
      const response = {
        data: data.filter(record => record.id !== id),
      };
      setData(filterDataByRole(response.data)); // 更新表格數據並過濾
      alert('成功刪除資料！'); // 成功提示
      console.log('成功刪除資料，回應:', response.data);
    } catch (error) {
      console.error('刪除請求失敗:', error);
      alert('刪除失敗，請稍後重試！'); // 錯誤提示
    }
  };

  const handleEdit = (record) => {
    if (!isAdmin) return; // 如果不是管理員，則返回
    setFormData({
      id: record.id,
      user_id: record.user_id, // 新增 user_id
      unit_name: record.unit_name,
      farmer_name: record.farmer_name,
      phone: record.phone,
      fax: record.fax,
      mobile: record.mobile,
      address: record.address,
      email: record.email,
      total_area: record.total_area,
      notes: record.notes,
      Number: record.Number,
      LandParcelNumber: record.LandParcelNumber,
      Area: record.Area,
      Crop: record.Crop,
    });
  };

  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表1-1.使用者基本資料</h4>
        <FormField
          id="user_id"
          name="user_id"
          type="text"
          value={formData.user_id}
          onChange={handleChange}
          label="user_id:"
        />
        <FormField
          id="unit_name"
          name="unit_name"
          type="text"
          value={formData.unit_name}
          onChange={handleChange}
          label="單位名稱:"
        />
        <FormField
          id="farmer_name"
          name="farmer_name"
          type="text"
          value={formData.farmer_name}
          onChange={handleChange}
          label="經營農戶姓名:"
        />
        <FormField
          id="phone"
          name="phone"
          type="text"
          value={formData.phone}
          onChange={handleChange}
          label="聯絡電話:"
        />
        <FormField
          id="fax"
          name="fax"
          type="text"
          value={formData.fax}
          onChange={handleChange}
          label="傳真(選填)"
        />
        <FormField
          id="mobile"
          name="mobile"
          type="text"
          value={formData.mobile}
          onChange={handleChange}
          label="行動電話:"
        />
        <FormField
          id="address"
          name="address"
          type="text"
          value={formData.address}
          onChange={handleChange}
          label="地址:"
        />
        <FormField
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          label="電子郵件:"
        />
        <FormField
          id="total_area"
          name="total_area"
          type="text"
          value={formData.total_area}
          onChange={handleChange}
          label="栽培總面積:"
        />
        <FormField
          id="notes"
          name="notes"
          type="text"
          value={formData.notes}
          onChange={handleChange}
          label="備註:"
        />
        <FormField
          id="Number"
          name="Number"
          type="text"
          value={formData.Number}
          onChange={handleChange}
          label="編號:"
        />
        <FormField
          id="LandParcelNumber"
          name="LandParcelNumber"
          type="text"
          value={formData.LandParcelNumber}
          onChange={handleChange}
          label="農地地籍號碼:"
        />
        <FormField
          id="Area"
          name="Area"
          type="text"
          value={formData.Area}
          onChange={handleChange}
          label="面積:"
        />
        <FormField
        id="Crop"
        name="Crop"
        type="text"
        value={formData.Crop}
        onChange={handleChange}
        label="種植作物:"
      />
        <Button type="submit" disabled={loading}>
          {loading ? '儲存中...' : '儲存'}
        </Button>
      </Form>
      <Clearfix height="50px" />
      {/* 表格顯示 */}
      <table className="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>id</th>
            <th>user_id</th>
            <th>單位名稱</th>
            <th>經營農戶姓名</th>
            <th>聯絡電話</th>
            <th>傳真(選填)</th>
            <th>行動電話</th>
            <th>住 址</th>
            <th>e-mail</th>
            <th>栽培總面積</th>
            <th>備註</th>
            <th>編號</th>
            <th>農地地籍號碼</th>
            <th>面積</th>
            <th>種植作物</th>
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.user_id}</td>
              <td>{record.unit_name}</td>
              <td>{record.farmer_name}</td>
              <td>{record.phone}</td>
              <td>{record.fax}</td>
              <td>{record.mobile}</td>
              <td>{record.address}</td>
              <td>{record.email}</td>
              <td>{record.total_area}</td>
              <td>{record.notes}</td>
              <td>{record.Number}</td>
              <td>{record.LandParcelNumber}</td>
              <td>{record.Area}</td>
              <td>{record.Crop}</td>
              {isAdmin && (
                <td>
                <EditButton className="btn btn-warning btn-sm" onClick={() => handleEdit(record)}>更正</EditButton>
                <DeleteButton className="btn btn-danger btn-sm" onClick={() => handleDelete(record.id)}>刪除</DeleteButton>
              </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
      <Clearfix height="500px" />
    </div>
  );
};

export default Page01;