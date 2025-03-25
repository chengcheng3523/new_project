// 種子(苗)登記表
import React, { useState, useEffect, useContext, useCallback } from 'react';
import Clearfix from "../components/common/Clearfix";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import SelectField from '../components/common/SelectField';
import FieldSelect from '../components/common/FieldSelect';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';
import { useNavigate } from 'react-router-dom';
import moment from 'moment';

const Page02 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    crop: '',
    crop_variety: '',
    seed_source: '',
    seedling_purchase_date: '',
    seedling_purchase_type: '',
    seedling_purchase_type_other: '', // 新增：當選擇「購買來源」時的單位輸入
    notes: '',
  });

  const [validcrops, setvalidcrops] = useState([]);  // 儲存有效的 crop
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchValidCrops = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/valid_crops');
      setvalidcrops(response.data);  // 設置有效的 crop
    } catch (error) {
      console.error('無法獲取有效的 crop:', error);
      alert('無法載入有效的田區代號，請稍後再試！');
    }
  }, []);


  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form02');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, // 使用 land_parcel_number 作为唯一标识符
          user_id: item.user_id,
          crop: item.crop,
          crop_variety: item.crop_variety,
          seed_source: item.seed_source,
          seedling_purchase_date: item.seedling_purchase_date,
          seedling_purchase_type: item.seedling_purchase_type,
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
    fetchValidCrops(); // 組件加載時獲取有效的 crop
  }, [fetchData, fetchValidCrops, navigate, userId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    // 如果不是管理员并且字段是 user_id，则不更新该字段
    if (!isAdmin && name === 'user_id') {
      return;
    }
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
      // 如果選擇「購買來源」，則清空 seed_source_other，反之則清空 seed_source
      ...(name === 'seed_source' && value !== '購買來源' ? { seed_source_other: '' } : {}),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);


  // 合併「種子(苗)來源」和「種子(苗)來源 (購買來源)」
  const seed_source = formData.seed_source === '購買來源' ? formData.seed_source_other : formData.seed_source;

  try {
    let response;
    if (formData.id) {
      if (isAdmin) {
        response = await axios.put(`http://127.0.0.1:5000/api/form02/${formData.id}`, {
          ...formData,
          seed_source, 
        });
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form02', {
          user_id: userId,
          crop: formData.crop,
          crop_variety: formData.crop_variety,
          seedling_purchase_type: formData.seedling_purchase_type,
          seedling_purchase_date: formData.seedling_purchase_date,
          seed_source ,
          notes: formData.notes,
        });
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        crop: '',
        crop_variety: '',
        seed_source: '',
        seedling_purchase_date: '',
        seedling_purchase_type: '',
        seedling_purchase_type_other: '',
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/form02/${id}`);
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

    const isOtherUnit = !['自行育苗'].includes(record.seed_source);
    setFormData({
      id: record.id,
      crop: record.crop,
      crop_variety: record.crop_variety,

      seedling_purchase_type: record.seedling_purchase_type,
      seed_source: isOtherUnit ? '購買來源' : record.seed_source || '',
      seed_source_other: isOtherUnit ? record.seed_source : '',

      seedling_purchase_date: record.seedling_purchase_date, 
      notes: record.notes,
    });
  };



  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表2.種子(苗)登記表</h4>

        <FieldSelect
          name="crop"
          type="select"
          value={formData.crop}
          onChange={handleChange}
          label="栽培作物:"
          >
          <option value="">選擇作物</option>
          {validcrops.map((crop) => (
            <option key={crop} value={crop}>
              {crop}
            </option>
          ))}
        </FieldSelect>

        <FormField
          label="栽培品種"
          name="crop_variety"
          value={formData.crop_variety}
          onChange={handleChange}
          disabled={loading}
        />

        <SelectField
          label="種子(苗)來源"
          name="seed_source"
          value={formData.seed_source}
          onChange={handleChange}
          options={[
            { value: '自行育苗', label: '自行育苗' },
            { value: '購買來源', label: '購買來源' },
          ]}
        />
        {formData.seed_source === '購買來源' && (
          <FormField
            label="種子(苗)來源 (購買來源)"
            name="seed_source_other" // 修正 name，避免覆蓋 seed_source
            value={formData.seed_source_other} // 綁定正確的值
            onChange={handleChange}
          />
        )}

        <FormField
          label="育苗(購入)日期"
          name="seedling_purchase_date"
          type="date"
          value={moment(formData.seedling_purchase_date).format('YYYY-MM-DD')}  // 格式化为 YYYY-MM-DD
          onChange={handleChange}
          disabled={loading}
        />

        <SelectField
          label="育苗(購入)種類"
          name="seedling_purchase_type"
          value={formData.seedling_purchase_type}
          onChange={handleChange}
          
          options={[
            { value: '種子', label: '種子' },
            { value: '種苗', label: '種苗' },
            { value: '繁殖體', label: '繁殖體' },
          ]}
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
        <caption>表2.種子(苗)登記表</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>栽培作物</th>
            <th>栽培品種</th>
            <th>種子(苗)來源</th>
            <th>育苗(購入)日期</th>
            <th>育苗(購入)種類</th>
            <th>備註</th>
            {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.crop}</td>
              <td>{record.crop_variety}</td>
              <td>{record.seed_source || '-'}</td>
              <td>{moment(record.seedling_purchase_date).format('YYYY-MM-DD')}</td> 
              <td>{record.seedling_purchase_type || '-'}</td>
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


export default Page02;