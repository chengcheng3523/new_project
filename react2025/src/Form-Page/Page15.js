// 場地設施之保養、維修及清潔管理紀錄
import React, { useState, useEffect, useContext, useCallback } from 'react';
import Clearfix from "../components/common/Clearfix";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import SelectField from '../components/common/SelectField';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';
import { useNavigate } from 'react-router-dom';
// import moment from 'moment';

const Page15 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: '',
    user_id: userId,
    date: '',
    item: '',
    item_other: '', // 其他項目
    operation: '',
    operation_other: '', // 其他作業內容
    recorder: '',
    notes: '',
  });

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form15');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, // 使用 land_parcel_number 作为唯一标识符
          user_id: item.user_id,
          date: item.date,
          item: item.item,
          operation: item.operation,
          recorder: item.recorder,
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


  // 合併 項目 & 作業內容
  const operation = formData.operation === '其他' ? formData.operation_other : formData.operation;
  const item = formData.item === '其他' ? formData.item_other : formData.item;

  try {
    let response;
    if (formData.id) {
      if (isAdmin) {
        response = await axios.put(`http://127.0.0.1:5000/api/form15/${formData.id}`, {
          ...formData, 
          item,
          operation
        });
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form15', {
          user_id: userId, 
          date: formData.date,
          item ,
          operation ,
          recorder: formData.recorder,
          notes: formData.notes,
        });
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        date: '',
        item: '',
        item_other: '',
        operation: '',
        operation_other: '',
        recorder: '',
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/form15/${id}`);
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
    
    const isOtherOperation = !['清潔',"保養","維修"].includes(record.operation);
    const isOtherItem = ![
      '育苗場所', 
      '溫/網室', 
      '資材放置場所', 
      '倉庫與工具間', 
      '集貨場', 
      '包裝場'
    ].includes(record.item);
    setFormData({
      id: record.id,
      user_id: record.user_id,
      date: record.date,
      
      item: isOtherItem ? '其他' : record.item || '',
      item_other: isOtherItem ? record.item : '', 

      operation: isOtherOperation ? '其他' : record.operation || '',
      operation_other: isOtherOperation ? record.operation : '', 
      
      recorder: record.recorder,
      notes: record.notes,
    });
  };


  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表 15.場地設施之保養、維修及清潔管理紀錄</h4>
        <FormField
          label="日期"
          type="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
        />

        <SelectField
          label="項目" 
          name="item"
          value={formData.item}
          onChange={handleChange}
          
          options={[
            { value: '育苗場所', label: '育苗場所' },
            { value: '溫/網室', label: '溫/網室' },
            { value: '資材放置場所', label: '資材放置場所' },
            { value: '倉庫與工具間', label: '倉庫與工具間' },
            { value: '集貨場', label: '集貨場' },
            { value: '包裝場', label: '包裝場' },
            { value: '其他', label: '其他' },

          ]}
        />
        {formData.item === '其他' && (
          <FormField
            label="項目(其他)"
            name="item_other"
            value={formData.item_other}
            onChange={handleChange}
            
          />
        )}

        <SelectField
          label="作業內容"
          name="operation"
          value={formData.operation}
          onChange={handleChange}
          
          options={[
            { value: '清潔', label: '清潔' },
            { value: '維修', label: '維修' },
            { value: '保養', label: '保養' },
            { value: '其他', label: '其他' },
          ]}
        />
        {formData.operation === '其他' && (
          <FormField
            label="作業內容(其他)"
            name="operation_other"
            value={formData.operation_other}
            onChange={handleChange}
            
          />
        )}

        <FormField
          label="記錄人"
          name="recorder"
          value={formData.recorder}
          onChange={handleChange}
          
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
        <caption>表 15.場地設施之保養、維修及清潔管理紀錄</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>日期</th>
            <th>項目</th>
            <th>作業內容</th>
            <th>記錄人</th>
            <th>備註</th>
            {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.date}</td>
              <td>{record.item}</td>
              <td>{record.operation}</td>
              <td>{record.recorder}</td>
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
      <Clearfix height="100px" />
    </div>
  );
};


export default Page15;