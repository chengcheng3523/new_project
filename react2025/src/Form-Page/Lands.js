// 農地資訊
import React, { useState, useEffect, useContext, useCallback } from 'react';
import Clearfix from "../components/common/Clearfix";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';
import { useNavigate } from 'react-router-dom';

const Lands = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    number: '',
    land_parcel_number: '',
    area: '',
    crop: '',
    notes: '',
    
  });

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/land_parcels');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, // 使用 land_parcel_number 作为唯一标识符
          user_id: item.user_id,
          number: item.number,
          land_parcel_number: item.land_parcel_number,
          area: item.area,
          crop: item.crop,
          notes: item.notes,
          operation_date: item.operation_date,
          created_date: item.created_date,
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

    // if (formData.id === null) {
    //   alert('請選擇要更新的資料！');
    //   setLoading(false);
    //   return;
    // }
    // 继续执行更新或新增逻辑...
    try {
      let response; 
      if (formData.id) {
        // 更新現有資料，使用 PUT 請求
        if (isAdmin) {
          response = await axios.put(`http://127.0.0.1:5000/api/land_parcels/${formData.id}`, formData);
        } else {
          alert('您沒有權限更新資料！');
          setLoading(false);
          return;
        }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/land_parcels', { ...formData, user_id: userId });
      }
      fetchData();
      setFormData({
        id: null,
        user_id: userId, 
        number: '',
        land_parcel_number: '',
        area: '',
        crop: '',
        notes: '',

      });
      alert('成功儲存資料！');
      console.log('成功發送請求，回應:', response.data);
      navigate('/'); // 跳轉到主頁
    } catch (error) {
      console.error('發送請求失敗:', error);
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/land_parcels/${id}`);
      console.log('删除成功:', response.data);
      fetchData(); // 刷新数据
      alert('成功刪除資料！');
    } catch (error) {
      console.error('刪除請求失敗:', error.response ? error.response.data : error.message);
      alert('刪除失敗，請稍後重試！');
    }
  };
  

  const handleEdit = (record) => {
    if (!isAdmin) return;
    console.log(record); // 确认记录内容
    setFormData({
      id: record.id,
      user_id: record.user_id,
      number: record.number,
      land_parcel_number: record.land_parcel_number,
      area: record.area,
      crop: record.crop,
      notes: record.notes,
    });
  };

  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>農地資訊</h4>

        <FormField
          id="number"
          name="number"
          type="text"
          value={formData.number}
          onChange={handleChange}
          label="編號"
        />
        <FormField
          id="land_parcel_number"
          name="land_parcel_number"
          type="text"
          value={formData.land_parcel_number}
          onChange={handleChange}
          label="農地地籍號碼"
        />
        <FormField
          id="area"
          name="area"
          type="text"
          value={formData.area}
          onChange={handleChange}
          label="面積（公頃）"
        />
        <FormField
          id="crop"
          name="crop"
          type="text"
          value={formData.crop}
          onChange={handleChange}
          label="種植作物"
        />
        <FormField
          id="notes"
          name="notes"
          type="text"
          value={formData.notes}
          onChange={handleChange}
          label="備註"
        />
        <Button type="submit" disabled={loading}>
          {loading ? '儲存中...' : '儲存'}
        </Button>
      </Form>
      <Clearfix height="50px" />
      {/* 表格顯示 */}
      <table className="table table-bordered table-hover table-responsive table caption-top">
        <caption>農地資訊</caption>
      <thead class="table-light">
          <tr>
            <th>id</th>
            <th>編號</th>
            <th>農地地籍號碼</th>
            <th>面積（公頃）</th>
            <th>種植作物</th>
            <th>備註</th>
            {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
                <td>{record.id}</td>
                <td>{record.number}</td>
                <td>{record.land_parcel_number}</td>
                <td>{record.area}</td>
                <td>{record.crop}</td>
                <td>{record.notes}</td>
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

export default Lands;
