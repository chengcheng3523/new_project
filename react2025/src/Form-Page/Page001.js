// 使用者基本資料
import React, { useState, useEffect, useContext ,useCallback } from 'react';
import Clearfix from "../components/common/Clearfix";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import moment from 'moment';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';
import { useNavigate } from 'react-router-dom';

const Page001 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role?.toLowerCase() === "admin"; // 判斷是否為管理員
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId,
    unit_name: '',
    farmer_name: '',
    phone: '',
    fax: '',
    mobile: '',
    address: '',
    email: '',
    total_area: '',
    notes: '',
    land_parcel_id: '',

  });

  const [data, setData] = useState([]); // 保存數據到狀態 
  const [loading, setLoading] = useState(false); // 控制提交按鈕的加載狀態
  const navigate = useNavigate();

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/users/get');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id,  // 使用对象字段而非数组索引
          user_id: item.username,  // 假设 'username' 对应于 user_id
          unit_name: item.unit_name,
          farmer_name: item.farmer_name,
          phone: item.phone,
          fax: item.fax,
          mobile: item.mobile,
          address: item.address,
          email: item.email,
          total_area: item.total_area,
          notes: item.notes,
          land_parcel_id: item.land_parcel_id,  // 需要确认该字段是否在数据中
        }));
 
        setData( transformedData ); // 設置數據狀態
        console.log('Data state after setting:', transformedData ); 
      } else {
        alert('伺服器返回錯誤，請稍後重試！');
      }
    } catch (error) {
      console.error('獲取數據失敗:', error);
      alert('無法載入數據，請檢查您的伺服器或網絡連接！');
    }
  }, [ ]);

  useEffect(() => {
    if (!userId) {
      alert('請先登入！');
      navigate('/login'); // 重定向到登入頁面
      return;
    }
    fetchData(); // 組件加載時獲取數據
  }, [fetchData, navigate, userId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    // 如果不是管理员并且字段是 user_id，则不更新该字段
    if (!isAdmin && name === 'user_id') {
      return;
    }
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // 阻止表單默認提交行為
    setLoading(true); // 開啟加載狀態

    // 格式化日期為 MySQL 支持的格式
    if (formData.OperationDate) {
      formData.OperationDate = moment(formData.OperationDate).format('YYYY-MM-DD HH:mm:ss');
    }

    try {

      let response;
      if (formData.id) {

        // 如果是管理員，則可以更新現有資料
        if (isAdmin) {
        // 更新現有資料
        response = await axios.put(`http://127.0.0.1:5000/api/users/${formData.id}`, formData);
        } else {
          alert('您沒有權限更新資料！');
          setLoading(false);
          return;
        }

      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/users/post', formData);
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        unit_name: '',
        farmer_name: '',
        phone: '',
        fax: '',
        mobile: '',
        address: '',
        email: '',
        total_area: '',
        notes: '',
        land_parcel_id: '',
      }); // 清空表單
      alert('成功儲存資料！'); // 成功提示
      console.log('成功發送請求，回應:', response.data);
      navigate('/'); // 跳轉到主頁
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
      await axios.delete(`http://127.0.0.1:5000/api/users/${id}`);
      fetchData(); // 重新獲取數據
      alert('成功刪除資料！'); // 成功提示

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
      land_parcel_id: record.land_parcel_id,
    });
  };

  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表1-1.使用者基本資料</h4>
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
          id="land_parcel_id"
          name="land_parcel_id"
          type="text"
          value={formData.land_parcel_id}
          onChange={handleChange}
          label="農地區號:" 
        />
        <Button type="submit" disabled={loading}>
          {loading ? '儲存中...' : '儲存'}
        </Button>
      </Form>
      <Clearfix height="50px" />
      {/* 表格顯示 */}
      <table className="table table-bordered table-hover table-responsive table caption-top">
        <caption>使用者基本資料</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>帳號</th>
            <th>單位名稱</th>
            <th>經營農戶姓名</th>
            <th>聯絡電話</th>
            <th>傳真(選填)</th>
            <th>行動電話</th>
            <th>住 址</th>
            <th>e-mail</th>
            <th>栽培總面積</th>
            <th>備註</th>
            <th>農地區號</th>
            {isAdmin && <th>操作</th>} {/* 只有管理员显示操作按钮 */}
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
              <td>{record.land_parcel_id}</td>
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

export default Page001;