// 生產計畫
import React, { useState, useEffect, useContext, useCallback } from 'react';
import Clearfix from "../components/common/Clearfix";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import FieldSelect from '../components/common/FieldSelect';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';
import { useNavigate } from 'react-router-dom';

const Page002 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    area_code: '',
    area_size: '',
    month: '',
    crop_info: '',
    notes: '',
  });

  const [validAreaCodes, setValidAreaCodes] = useState([]);  // 儲存有效的 area_code
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // 請求所有有效的 area_code
  const fetchValidAreaCodes = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/valid_area_codes');
      setValidAreaCodes(response.data);  // 設置有效的 area_code
    } catch (error) {
      console.error('無法獲取有效的 area_codes:', error);
      alert('無法載入有效的田區代號，請稍後再試！');
    }
  }, []);

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form002');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id,
          user_id: item.user_id,
          area_code: item.area_code,
          area_size: item.area_size,
          month: item.month,
          crop_info: item.crop_info,
          notes: item.notes,
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
    fetchValidAreaCodes(); // 加載有效的 area_code
    fetchData(); // 組件加載時獲取數據
  }, [fetchValidAreaCodes,fetchData, navigate, userId]);

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
        response = await axios.put(`http://127.0.0.1:5000/api/form002/${formData.id}`, formData);
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form002', {
          user_id: userId,
          area_code: formData.area_code,
          area_size: formData.area_size,
          month: formData.month,
          crop_info: formData.crop_info,
          notes: formData.notes,
        });
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        area_code: '',
        area_size: '',
        month: '',
        crop_info: '',
        notes: '',
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/form002/${id}`);
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
      area_code: record.area_code,
      area_size: record.area_size,
      month: record.month,
      crop_info: record.crop_info,
      notes: record.notes,
    });
  };

  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表1-2.生產計畫</h4>
        <FieldSelect
          label="田區代號"
          name="area_code"
          value={formData.area_code}
          onChange={handleChange}
          type="select"
        >
          <option value="">選擇田區代號</option>
          {validAreaCodes.map((areaCode) => (
            <option key={areaCode} value={areaCode}>
              {areaCode}
            </option>
          ))}
        </FieldSelect>
        <FormField
          label="場區面積(公頃)"
          name="area_size"
          value={formData.area_size}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="月份"
          name="month"
          value={formData.month}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="種植作物種類、產期、預估產量（公斤）"
          name="crop_info"
          value={formData.crop_info}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="備註"
          name="notes"
          value={formData.notes}
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
        <caption>生產計畫</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>場區代號</th>
            <th>場區面積</th>
            <th>月份</th>
            <th>種植作物種類、產期、預估產量(公斤)ex：小白菜/1000</th>
            <th>備註</th>
            {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.area_code}</td>
              <td>{record.area_size}</td>
              <td>{record.month}</td>
              <td>{record.crop_info}</td>
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

export default Page002;