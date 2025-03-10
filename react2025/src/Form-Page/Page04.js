// 養液配製
import React, { useState, useEffect, useContext, useCallback } from 'react';
import Clearfix from "../components/common/Clearfix";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
// import SelectField from '../components/common/SelectField';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';
import { useNavigate } from 'react-router-dom';

const Page04 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    preparation_date: '',
    material_code_or_name: '',
    usage_amount: '',
    preparation_process: '',
    final_ph_value: '',
    final_ec_value: '',
    preparer_name: '',
    notes: '',
  });

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form04');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id,  
          user_id: item.user_id,
          preparation_date: item.preparation_date,
          material_code_or_name: item.material_code_or_name,
          usage_amount: item.usage_amount,
          preparation_process: item.preparation_process,
          final_ph_value: item.final_ph_value,
          final_ec_value: item.final_ec_value,
          preparer_name: item.preparer_name,
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

  // 檢查必要欄位是否填寫
  const requiredFields = ['preparation_date', 'material_code_or_name', 'usage_amount', 'preparation_process', 'final_ph_value', 'final_ec_value', 'preparer_name'];
  for (const field of requiredFields) {
    if (!formData[field]) {
      alert(`請填寫 ${field} 欄位！`);
      setLoading(false);
      return;
    }
  }

  try {
    let response;
    if (formData.id) {
      // 更新現有資料，使用 PUT 請求
      if (isAdmin) {
        response = await axios.put(`http://127.0.0.1:5000/api/form04/${formData.id}`, formData);
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form04', {
          user_id: userId,
          preparation_date: formData.preparation_date,
          material_code_or_name: formData.material_code_or_name,
          usage_amount: formData.usage_amount,
          preparation_process: formData.preparation_process,
          final_ph_value: formData.final_ph_value,
          final_ec_value: formData.final_ec_value,
          preparer_name: formData.preparer_name,
          notes: formData.notes,
        });
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        preparation_date: '',
        material_code_or_name: '',
        usage_amount: '',
        preparation_process: '',
        final_ph_value: '',
        final_ec_value: '',
        preparer_name: '',
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/form04/${id}`);
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
      preparation_date: record.preparation_date,
      material_code_or_name: record.material_code_or_name,
      usage_amount: record.usage_amount,
      preparation_process: record.preparation_process,
      final_ph_value: record.final_ph_value,
      final_ec_value: record.final_ec_value,
      preparer_name: record.preparer_name,
      notes: record.notes,
    });
  };

  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表 4.養液配製紀錄</h4>
        <FormField
          label="配製日期"
          id="preparation_date"
          name="preparation_date"
          value={formData.preparation_date}
          onChange={handleChange}
          type="date"
        />
        <FormField
          label="資材代碼或資材名稱"
          id="material_code_or_name"
          name="material_code_or_name"
          value={formData.material_code_or_name}
          onChange={handleChange}
        />
        <FormField
          label="使用量(公斤/公升)"
          id="usage_amount"
          name="usage_amount"
          value={formData.usage_amount}
          onChange={handleChange}
        />
        <FormField
          label="配製流程簡述"
          id="preparation_process"
          name="preparation_process"
          value={formData.preparation_process}
          onChange={handleChange}
        />
        <FormField
          label="最終PH值"
          id="final_ph_value"
          name="final_ph_value"
          value={formData.final_ph_value}
          onChange={handleChange}
        />
        <FormField
          label="最終EC值(mS/cm)"
          name="final_ec_value"
          value={formData.final_ec_value}
          onChange={handleChange}
        />
        <FormField
          label="配製人員名稱"
          name="preparer_name"
          value={formData.preparer_name}
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
        <caption>養液配製紀錄</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>配製日期</th>
            <th>資材代碼或資材名稱</th>
            <th>使用量(公斤/公升)</th>
            <th>配製流程簡述</th>
            <th>最終PH值</th>
            <th>最終EC值(mS/cm)</th>
            <th>配製人員名稱</th>
            <th>備註</th>
            </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.preparation_date}</td>
              <td>{record.material_code_or_name}</td>
              <td>{record.usage_amount}</td>
              <td>{record.preparation_process}</td>
              <td>{record.final_ph_value}</td>
              <td>{record.final_ec_value}</td>
              <td>{record.preparer_name}</td>
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

export default Page04;