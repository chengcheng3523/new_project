// 採收及採後處理紀錄
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

const Page17 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: '',
    user_id: userId,
    harvest_date: '',
    field_code: '',
    crop_name: '',
    batch_or_trace_no: '',
    harvest_weight: '',
    process_date: '',
    post_harvest_treatment: '', //採後處理內容
    post_harvest_treatment_other: '', //  採後處理內容(其他)
    post_treatment_weight: '', // 處理後重量(公斤)
    verification_status: '', // 驗證狀態
    verification_status_other: '', // 驗證狀態(其他)
    notes: '',
  });

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form17');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, // 使用 land_parcel_number 作为唯一标识符
          user_id: item.user_id,
          harvest_date: item.harvest_date,
          field_code: item.field_code,
          crop_name: item.crop_name,
          batch_or_trace_no: item.batch_or_trace_no,
          harvest_weight: item.harvest_weight,
          process_date: item.process_date,
          post_harvest_treatment: item.post_harvest_treatment,
          post_treatment_weight: item.post_treatment_weight,
          verification_status: item.verification_status,
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

  // 合併 驗證狀態 & 採後處理內容
  const verification_status= formData.verification_status=== '驗證產品' ? formData.verification_status_other : formData.verification_status;
  const post_harvest_treatment= formData.post_harvest_treatment=== '其他' ? formData.post_harvest_treatment_other : formData.post_harvest_treatment;

  try {
    let response;
    if (formData.id) {
      if (isAdmin) {
        response = await axios.put(`http://127.0.0.1:5000/api/form17/${formData.id}`, {
          ...formData, 
          post_harvest_treatment,
          verification_status
        });
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form17', {
          user_id: userId, 
          harvest_date: formData.harvest_date,
          field_code: formData.field_code,
          crop_name: formData.crop_name,
          batch_or_trace_no: formData.batch_or_trace_no,
          harvest_weight: formData.harvest_weight,
          process_date: formData.process_date,
          post_harvest_treatment,
          verification_status, 
          post_treatment_weight: formData.post_treatment_weight,
          notes: formData.notes,
        });
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        harvest_date: '',
        field_code: '',
        crop_name: '',
        batch_or_trace_no: '',
        harvest_weight: '',
        process_date: '',
        post_harvest_treatment: '',
        post_harvest_treatment_other: '',
        post_treatment_weight: '',
        verification_status: '',
        verification_status_other: '', 
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/form17/${id}`);
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
    
    const isOtherVerification_status= !['非驗證產品'].includes(record.verification_status);
    const isOtherpost_harvest_treatment= ![
      '清洗', 
      '整修', 
      '去雜', 
      '分級', 
      '預冷', 
      '冷藏',
      '去殼/去莢',
    ].includes(record.post_harvest_treatment);
    setFormData({
      id: record.id,
      user_id: record.user_id,
      harvest_date: record.harvest_date,
      field_code: record.field_code,
      crop_name: record.crop_name,
      batch_or_trace_no: record.batch_or_trace_no,
      harvest_weight: record.harvest_weight,
      process_date: record.process_date,
      
      post_harvest_treatment: isOtherpost_harvest_treatment? '其他' : record.post_harvest_treatment|| '',
      post_harvest_treatment_other: isOtherpost_harvest_treatment? record.post_harvest_treatment: '', 
      
      post_treatment_weight: record.post_treatment_weight,
      
      verification_status: isOtherVerification_status? '驗證產品' : record.verification_status|| '',
      verification_status_other: isOtherVerification_status? record.verification_status: '', 
       
      notes: record.notes,
    });
  };


  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表 17.採收及採後處理紀錄</h4>
        <FormField
          label="採收日期"
          type="date"
          name="harvest_date"
          value={formData.harvest_date}
          onChange={handleChange}
        />
        <FormField
          label="田區代號"
          name="field_code"
          value={formData.field_code}
          onChange={handleChange}
        />
        <FormField
          label="作物名稱"
          name="crop_name"
          value={formData.crop_name}
          onChange={handleChange}
        />
        <FormField
          label="批次編號或履歷編號"
          name="batch_or_trace_no"
          value={formData.batch_or_trace_no}
          onChange={handleChange}
        />
        <FormField
          label="採收重量(處理前)(公斤)"
          name="harvest_weight"
          value={formData.harvest_weight}
          onChange={handleChange}
        />
        <FormField
          label="處理日期"
          type="date"
          name="process_date"
          value={formData.process_date}
          onChange={handleChange}
        />
        <SelectField
          label="採後處理內容" 
          name="post_harvest_treatment"
          value={formData.post_harvest_treatment}
          onChange={handleChange}
          required
          options={[
            { value: '清洗', label: '清洗' },
            { value: '整修', label: '整修' },
            { value: '去雜', label: '去雜' },
            { value: '分級', label: '分級' },
            { value: '預冷', label: '預冷' },
            { value: '冷藏', label: '冷藏' },
            { value: '去殼/去莢', label: '去殼/去莢' }, 
            { value: '其他', label: '其他' },

          ]}
        />
        {formData.post_harvest_treatment=== '其他' && (
          <FormField
            label="採後處理內容(其他)"
            name="post_harvest_treatment_other"
            value={formData.post_harvest_treatment_other}
            onChange={handleChange}
            required
          />
        )}

        <FormField
        label="處理後重量(公斤)"
        name="post_treatment_weight"
        value={formData.post_treatment_weight}
        onChange={handleChange}
        />

        <SelectField
          label="驗證狀態"
          name="verification_status"
          value={formData.verification_status}
          onChange={handleChange}
          required
          options={[
            { value: '非驗證產品', label: '非驗證產品' },
            { value: '驗證產品', label: '驗證產品' },
          ]}
        />
        {formData.verification_status=== '驗證產品' && (
          <FormField
            label="驗證產品，驗證機構："
            name="verification_status_other"
            value={formData.verification_status_other}
            onChange={handleChange}
            required
          />
        )}
 
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
        <caption>表 17.採收及採後處理紀錄</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>採收日期</th>
            <th>田區代號</th>
            <th>作物名稱</th>
            <th>批次編號或履歷編號</th>
            <th>採收重量(處理前)(公斤)</th>
            <th>處理日期</th>

            <th>採後處理內容</th>
            <th>處理後重量(公斤)</th> 
            <th>驗證狀態</th>
            <th>備註</th>
            {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.harvest_date}</td>
              <td>{record.field_code}</td>
              <td>{record.crop_name}</td>
              <td>{record.batch_or_trace_no}</td>
              <td>{record.harvest_weight}</td>
              <td>{record.process_date}</td>

              <td>{record.post_harvest_treatment}</td>
              <td>{record.post_treatment_weight}</td>
              <td>{record.verification_status}</td>
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


export default Page17;