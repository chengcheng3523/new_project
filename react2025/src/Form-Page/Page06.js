// 肥料施用
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


const Page06 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    date_used: '',
    field_code: '',
    crop: '',
    fertilizer_type: '',
    material_code_or_name: '',
    fertilizer_amount: '',
    dilution_factor: '',
    operator: '',
    process: '',
    notes: '',
  });
  
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form06');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, // 使用 land_parcel_number 作为唯一标识符
          user_id: item.user_id,
          date_used: item.date_used,
          field_code: item.field_code,
          crop: item.crop,
          fertilizer_type: item.fertilizer_type,
          material_code_or_name: item.material_code_or_name,
          fertilizer_amount: item.fertilizer_amount,
          dilution_factor: item.dilution_factor,
          operator: item.operator,
          process: item.process,
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
  const requiredFields = ['date_used', 'field_code', 'crop', 'fertilizer_type', 'material_code_or_name', 'fertilizer_amount', 'dilution_factor', 'operator', 'process'];
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
        response = await axios.put(`http://127.0.0.1:5000/api/form06/${formData.id}`, formData);
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form06', {
          user_id: userId,
          date_used: formData.date_used,
          field_code: formData.field_code,
          crop: formData.crop,
          fertilizer_type: formData.fertilizer_type,
          material_code_or_name: formData.material_code_or_name,
          fertilizer_amount: formData.fertilizer_amount,
          dilution_factor: formData.dilution_factor,
          operator: formData.operator,
          process: formData.process,
          notes: formData.notes,
        });
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        date_used: '',
        field_code: '',
        crop: '',
        fertilizer_type: '',
        material_code_or_name: '',
        fertilizer_amount: '',
        dilution_factor: '',
        operator: '',
        process: '',
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/form06/${id}`);
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
      date_used: record.date_used,
      field_code: record.field_code,
      crop: record.crop,
      fertilizer_type: record.fertilizer_type,
      material_code_or_name: record.material_code_or_name,
      fertilizer_amount: record.fertilizer_amount,
      dilution_factor: record.dilution_factor,
      operator: record.operator,
      process: record.process,
      notes: record.notes,
    });
  };
  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表 6.肥料施用紀錄</h4>
        <FormField
          label="使用日期"
          id="date_used"
          name="date_used"
          type={'date'}
          value={formData.date_used}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="田區代號"
          name="field_code"
          value={formData.field_code}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="作物"
          name="crop"
          value={formData.crop}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="施肥別 (基肥, 追肥)"
          name="fertilizer_type"
          value={formData.fertilizer_type}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="資材代碼或資材名稱"
          name="material_code_or_name"
          value={formData.material_code_or_name}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="肥料使用量 (公斤/公升)"
          name="fertilizer_amount"
          value={formData.fertilizer_amount}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="稀釋倍數"
          name="dilution_factor"
          value={formData.dilution_factor}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="操作人員"
          name="operator"
          value={formData.operator}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="製作流程"
          name="process"
          value={formData.process}
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
        <caption>肥料施用紀錄</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>使用日期</th>
            <th>田區代號</th>
            <th>作物</th>
            <th>施肥別 (基肥, 追肥)</th>
            <th>資材代碼或資材名稱</th>
            <th>肥料使用量 (公斤/公升)</th>
            <th>稀釋倍數</th>
            <th>操作人員</th>
            <th>製作流程</th>
            <th>備註</th>
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.date_used}</td>
              <td>{record.field_code}</td>
              <td>{record.crop}</td>
              <td>{record.fertilizer_type}</td>
              <td>{record.material_code_or_name}</td>
              <td>{record.fertilizer_amount}</td>
              <td>{record.dilution_factor}</td>
              <td>{record.operator}</td>
              <td>{record.process}</td>
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

export default Page06;