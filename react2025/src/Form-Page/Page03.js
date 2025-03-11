// 栽培工作紀錄
import React, { useState, useEffect, useContext, useCallback } from 'react';
import Clearfix from "../components/common/Clearfix";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import MultiSelectField  from '../components/common/MultiSelectField';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';
import { useNavigate } from 'react-router-dom';


const Page03 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    operation_date: '',
    field_code: '',
    crop: '',
    crop_content: '',
    crop_content_other: '', // 新增：當選擇「其他」時的單位輸入
    notes: '',
  });
  
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form03');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, // 使用 land_parcel_number 作为唯一标识符
          user_id: item.user_id,
          operation_date: item.operation_date,
          field_code: item.field_code,
          crop: item.crop,
          crop_content: item.crop_content,
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
  const requiredFields = ['operation_date', 'field_code', 'crop', 'crop_content' ];
  for (const field of requiredFields) {
    if (!formData[field]) {
      alert(`請填寫 ${field} 欄位！`);
      setLoading(false);
      return;
    }
  }

  // 合併 
  const crop_content = formData.crop_content === '其他' ? formData.crop_content_other : formData.crop_content;
 
  try {
    let response;
    if (formData.id) {
      if (isAdmin) {
        response = await axios.put(`http://127.0.0.1:5000/api/form03/${formData.id}`, {
          ...formData,
          crop_content, 
        });
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form03', {
          user_id: userId,
          operation_date: formData.operation_date,
          field_code: formData.field_code,
          crop: formData.crop,
          crop_content ,
          notes: formData.notes,
        });
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        operation_date: '',
        field_code: '',
        crop: '',
        crop_content: '', 
        crop_content_other: '',
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/form03/${id}`);
      console.log('删除成功:', response.data);
      fetchData(); // 刷新数据
      alert('成功刪除資料！');
    } catch (error) {
      alert(`刪除請求失敗：${error.response?.data?.message || error.message}`);
      console.error('刪除請求失敗:', error.response ? error.response.data : error.message); 
    }
  };


  const handleEdit = (record) => {
    if (!isAdmin) return; // 如果不是管理員，則返回 

    const isOtherUnit = ![
      '(1-1) 整地', '(1-2) 作畦', '(1-3) 配置灌溉/澆水管線',
      '(1-4) 土壤改良', '(1-5) 土壤消毒', '(1-6) 設施操作',
      '(1-7) 開溝', '(1-8) 清園', '(1-9) 立支柱',
      '(1-10)遮蔭網', '(2-1) 介質消毒', '(2-2) 裝袋作業',
      '(2-3) 上架', '(2-4) 介質調配', '(2-5) 養液配置',
      '(3-1) 播種', '(3-2) 育苗', '(3-3) 定植(移植)',
      '(3-4) 播種前種子處理', '(4-1) 中耕', '(4-2) 灌溉/澆水',
      '(4-3) 培土', '(4-4) 摘葉', '(4-5) 缺株補植',
      '(4-6) 整蔓', '(4-7) 授粉', '(4-8) 套袋',
      '(5-1) 基肥', '(5-2) 追肥', '(5-3) 液肥',
      '(6-1) 施用防治資材', '(6-2) 栽培防治', '(6-3) 物理防治',
      '(6-4) 生物防治', '(6-5) 忌避作物', '(6-6) 除草',
      '(6-7) 覆蓋','(7-1) 採收', '(7-2) 產季結束'
    ].includes(record.crop_content);
    setFormData({
      id: record.id,
      operation_date: record.operation_date,
      field_code: record.field_code,
      crop: record.crop,
      crop_content: isOtherUnit ? '其他' : record.crop_content || '',
      crop_content_other: isOtherUnit ? record.crop_content : '',
      notes: record.notes,
    });
  };
  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表3.栽培工作紀錄</h4>
        <FormField
          id="operation_date"
          name="operation_date"
          type="date"
          value={formData.operation_date}
          onChange={handleChange}
          label="作業日期:"
        />
        <FormField
          id="field_code"
          name="field_code"
          type="text"
          value={formData.field_code}
          onChange={handleChange}
          label="田區代號:"
        />

        <FormField
          id="crop"
          name="crop"
          type="text"
          value={formData.crop}
          onChange={handleChange}
          label="作物:"
        />
        <MultiSelectField 
          label="作業內容(可填寫代碼)"
          name="crop_content"
          value={formData.crop_content}
          onChange={handleChange}
          required
          options={[
            { value: '(1-1) 整地', label: '(1-1) 整地' },
            { value: '(1-2) 作畦', label: '(1-2) 作畦' },
            { value: '(1-3) 配置灌溉/澆水管線', label: '(1-3) 配置灌溉/澆水管線' },
            { value: '(1-4) 土壤改良', label: '(1-4) 土壤改良' },
            { value: '(1-5) 土壤消毒', label: '(1-5) 土壤消毒' },
            { value: '(1-6) 設施操作', label: '(1-6) 設施操作' },
            { value: '(1-7) 開溝', label: '(1-7) 開溝' },
            { value: '(1-8) 清園', label: '(1-8) 清園' },
            { value: '(1-9) 立支柱', label: '(1-9) 立支柱' },
            { value: '(1-10)遮蔭網', label: '(1-10)遮蔭網' },
            { value: '(2-1) 介質消毒', label: '(2-1) 介質消毒' },
            { value: '(2-2) 裝袋作業', label: '(2-2) 裝袋作業' },
            { value: '(2-3) 上架', label: '(2-3) 上架' },
            { value: '(2-4) 介質調配', label: '(2-4) 介質調配' },
            { value: '(2-5) 養液配置', label: '(2-5) 養液配置' },
            { value: '(3-1) 播種', label: '(3-1) 播種' },
            { value: '(3-2) 育苗', label: '(3-2) 育苗' },
            { value: '(3-3) 定植(移植)', label: '(3-3) 定植(移植)' },
            { value: '(3-4) 播種前種子處理', label: '(3-4) 播種前種子處理' },
            { value: '(4-1) 中耕', label: '(4-1) 中耕' },
            { value: '(4-2) 灌溉/澆水', label: '(4-2) 灌溉/澆水' },
            { value: '(4-3) 培土', label: '(4-3) 培土' },
            { value: '(4-4) 摘葉', label: '(4-4) 摘葉' },
            { value: '(4-5) 缺株補植', label: '(4-5) 缺株補植' },
            { value: '(4-6) 整蔓', label: '(4-6) 整蔓' },
            { value: '(4-7) 授粉', label: '(4-7) 授粉' },
            { value: '(4-8) 套袋', label: '(4-8) 套袋' },
            { value: '(5-1) 基肥', label: '(5-1) 基肥' },
            { value: '(5-2) 追肥', label: '(5-2) 追肥' },
            { value: '(5-3) 液肥', label: '(5-3) 液肥' },
            { value: '(6-1) 施用防治資材', label: '(6-1) 施用防治資材' },
            { value: '(6-2) 栽培防治', label: '(6-2) 栽培防治' },
            { value: '(6-3) 物理防治', label: '(6-3) 物理防治' },
            { value: '(6-4) 生物防治', label: '(6-4) 生物防治' },
            { value: '(6-5) 忌避作物', label: '(6-5) 忌避作物' },
            { value: '(6-6) 除草', label: '(6-6) 除草' },
            { value: '(6-7) 覆蓋', label: '(6-7) 覆蓋' },
            { value: '(7-1) 採收', label: '(7-1) 採收' },
            { value: '(7-2) 產季結束', label: '(7-2) 產季結束' },
            { value: '其他', label: '其他' },
          ]}
          />
          {formData.crop_content === '其他' && (
            <FormField
              label="其他"
              name="crop_content_other"
              value={formData.crop_content_other}
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
        <caption>.栽培工作紀錄</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>作業日期</th>
            <th>田區代號</th>
            <th>作物</th>
            <th>作業內容</th>
            <th>備註</th>
            {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.operation_date}</td>
              <td>{record.field_code}</td>
              <td>{record.crop}</td>
              <td>{record.crop_content || '-'}</td>
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

export default Page03;