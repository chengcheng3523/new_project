// 表 22.客戶抱怨/回饋紀錄 

import React, { useState, useEffect, useContext, useCallback } from 'react';
import Clearfix from "../components/common/Clearfix";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField'; 
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';
import { useNavigate } from 'react-router-dom';

const Page22 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    date: '',
    customer_name: '',
    customer_phone: '', 
    complaint: '',
    resolution: '', 
    processor_name: '', 
    processor_date: '',
  });
  
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form22');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, // 使用 land_parcel_number 作为唯一标识符
          user_id: item.user_id,
          date: item.date,
          customer_name: item.customer_name,
          customer_phone: item.customer_phone, 
          complaint: item.complaint,
          resolution: item.resolution, 
          processor_name: item.processor_name, 
          processor_date: item.processor_date,
        }));

        setData(transformedData);
        console.log('Data state after setting:', transformedData);
      } else {
        alert('伺服器返回錯誤，請稍後重試！');
      }
    } catch (error) {
      console.error('獲取數據失敗:', error);
      alert('無法載入數據，請檢查您的伺服器或網絡連接！');
    }
  }, []);


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
    e.preventDefault();
    setLoading(true);


  try {
    let response;
    if (formData.id) {
      // 更新現有資料，使用 PUT 請求
      if (isAdmin) {
        response = await axios.put(`http://127.0.0.1:5000/api/form22/${formData.id}`, formData);
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form22', {
          user_id: userId,
          date: formData.date,
          customer_name: formData.customer_name,
          customer_phone: formData.customer_phone, 
          complaint: formData.complaint,
          resolution: formData.resolution, 
          processor_name: formData.processor_name, 
          processor_date: formData.processor_date,
        });
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        date: '',
        customer_name: '',
        customer_phone: '', 
        complaint: '',
        resolution: '', 
        processor_name: '', 
        processor_date: '',
      });
      alert('成功儲存資料！');
      console.log('成功發送請求，回應:', response.data);
      navigate('/'); // 跳轉到主頁
    } catch (error) {
      console.error('發送請求失敗:', error.response ? error.response.data : error.message);
      alert('儲存失敗，請稍後重試！');
    } finally {
      setLoading(false);
    }
  };
  const handleDelete = async (id) => {
    if (!isAdmin) return;
    console.log('要刪除的 ID:', id); // 确认要删除的 ID
    if (!id) {
      alert('無效的 ID，無法刪除！');
      return;
    }
    try {
      const response = await axios.delete(`http://127.0.0.1:5000/api/form22/${id}`);
      console.log('删除成功:', response.data);
      fetchData(); // 刷新数据
      alert('成功刪除資料！');
    } catch (error) {
      console.error('刪除請求失敗:', error.response ? error.response.data : error.message);
      alert('刪除失敗，請稍後重試！');
    }
  };


  const handleEdit = (record) => {
    if (!isAdmin) return; // 如果不是管理員，則返回
    setFormData({
      id: record.id,
      date: record.date,
      customer_name: record.customer_name,
      customer_phone: record.customer_phone, 
      complaint: record.complaint,
      resolution: record.resolution, 
      processor_name: record.processor_name, 
      processor_date: record.processor_date,
    });
  };
  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表 22.客戶抱怨/回饋紀錄</h4>
        <FormField
          label="日期"
          id="date"
          name="date"
          type={'date'}
          value={formData.date}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="客戶名稱"
          name="customer_name"
          value={formData.customer_name}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="客戶電話"
          name="customer_phone"
          value={formData.customer_phone}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="客訴內容"
          name="complaint"
          value={formData.complaint}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="處理結果"
          name="resolution"
          value={formData.resolution}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="處理人簽名"
          name="processor_name"
          value={formData.processor_name}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="簽名日期"
          name="processor_date"
          value={formData.processor_date}
          type={'date'}
          onChange={handleChange}
          disabled={loading}
        />
        <Button type="submit" disabled={loading}>
          {loading ? '儲存中...' : '儲存'}
        </Button>
      </Form>
      <Clearfix height="50px" />
      {/* 表格顯示 */}
      <table className="table table-bordered table-hover table-responsive table caption-top">
        <caption>客戶抱怨/回饋紀錄</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>日期</th>
            <th>客戶名稱</th>
            <th>客戶電話</th> 
            <th>客訴內容</th>
            <th>處理結果</th> 
            <th>處理人簽名</th> 
            <th>簽名日期</th>
            {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.date}</td>
              <td>{record.customer_name}</td>
              <td>{record.customer_phone}</td> 
              <td>{record.complaint}</td>
              <td>{record.resolution}</td> 
              <td>{record.processor_name}</td> 
              <td>{record.processor_date}</td>
              {isAdmin && (
                <td>
                <EditButton className="btn btn-warning btn-sm" onClick={() => handleEdit(record)}>更正</EditButton>
                <DeleteButton className="btn btn-danger btn-sm" onClick={() => {
                  console.log('删除请求的ID:', record.id);  // 打印 ID，检查是否为 undefined
                  handleDelete(record.id);
                }}>
                  刪除
                </DeleteButton>
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

export default Page22;







