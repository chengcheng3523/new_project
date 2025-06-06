// 肥料入出庫
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
import moment from 'moment';

const Page08 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    fertilizer_material_name: '',
    manufacturer: '',
    supplier : '',
    date: '',
    packaging_unit : '',
    packaging_volume : '',
    purchase_quantity : '',
    usage_quantity : '',
    remaining_quantity : '',
    notes: '',
  });

  const [fertilizerOptions, setFertilizerOptions] = useState([]);  // 儲存有效的資材名稱
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // 請求所有有效的資材名稱
  const fetchFertilizerOptions = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/fertilizer-options');
      setFertilizerOptions(response.data);  // 設置有效的資材名稱
    } catch (error) {
      console.error('無法獲取有效的資材名稱:', error);
      alert('無法載入有效的資材名稱，請稍後再試！');
    }
  }, []);

  // 根據選擇的資材名稱查詢資料
  const fetchMaterialFertilizer = useCallback(async (fertilizerMaterialName) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/form07/material/${fertilizerMaterialName}`);
      if (response.data) {
        const { manufacturer, supplier, packaging_unit, packaging_volume } = response.data;
        setFormData(prev => ({
          ...prev,
          manufacturer,
          supplier,
          packaging_unit,
          packaging_volume,
        }));
      }
    } catch (error) {
      console.error('無法查詢肥料資材詳細資料:', error);
    }
  }, []);

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form08');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, 
          user_id: item.user_id,
          fertilizer_material_name: item.fertilizer_material_name,
          manufacturer: item.manufacturer,
          supplier: item.supplier,
          date: item.date,
          packaging_unit: item.packaging_unit,
          packaging_volume: item.packaging_volume,
          purchase_quantity: item.purchase_quantity,
          usage_quantity: item.usage_quantity,
          remaining_quantity: item.remaining_quantity,
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
      fetchFertilizerOptions(); // 組件加載時獲取有效的資材名稱
      setFormData(prev => ({ ...prev, user_id: userId })); // 動態更新 user_id 
      fetchData(); // 組件加載時獲取數據

      if (formData.fertilizer_material_name) {
        fetchMaterialFertilizer(formData.fertilizer_material_name);
      }
    }, [fetchData, fetchFertilizerOptions, fetchMaterialFertilizer, navigate, userId, formData.fertilizer_material_name]);
  
    const handleChange = (e) => {
      const { name, value } = e.target;
      if (!isAdmin && name === 'user_id') return;

      // 自動計算剩餘量
      let newFormData = { ...formData, [name]: value };

      if (name === 'purchase_quantity' || name === 'usage_quantity') {
        const purchase = parseFloat(newFormData.purchase_quantity) || 0;
        const usage = parseFloat(newFormData.usage_quantity) || 0;
        newFormData.remaining_quantity = (purchase - usage).toFixed(2);  // 自動更新剩餘量
      }

      setFormData(newFormData);
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
  

  try {
    let response;
    if (formData.id) {
      if (isAdmin) {
        response = await axios.put(`http://127.0.0.1:5000/api/form08/${formData.id}`, {
          ...formData,
        });
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form08', {
          user_id: userId,
          fertilizer_material_name: formData.fertilizer_material_name,
          manufacturer: formData.manufacturer,
          supplier: formData.supplier,
          date: formData.date,
          packaging_unit: formData.packaging_unit,
          packaging_volume: formData.packaging_volume,
          purchase_quantity: formData.purchase_quantity,
          usage_quantity: formData.usage_quantity,
          remaining_quantity: formData.remaining_quantity,
          notes: formData.notes,
        });
      }
      fetchData(); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId,
        fertilizer_material_name: '',
        manufacturer: '',
        supplier: '',
        date: '',
        packaging_unit: '',
        packaging_volume: '',
        purchase_quantity: '',
        usage_quantity: '',
        remaining_quantity: '',
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/form08/${id}`);
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
      user_id: record.user_id,
      fertilizer_material_name: record.fertilizer_material_name || '',
      manufacturer: record.manufacturer || '',
      supplier: record.supplier || '',
      date: record.date || '',
      packaging_unit: record.packaging_unit || '',
      packaging_volume: record.packaging_volume || '',
      purchase_quantity: record.purchase_quantity || '',
      usage_quantity: record.usage_quantity || '',
      remaining_quantity: record.remaining_quantity || '',
      notes: record.notes || '',
    });
  };

  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表 8.肥料入出庫紀錄</h4>

        {/* 資材名稱下拉選單 */}
        <FieldSelect
          name="fertilizer_material_name"
          type="select"
          value={formData.fertilizer_material_name}
          onChange={handleChange}
          label="資材名稱"
        >
          <option value="">選擇資材名稱</option>
          {fertilizerOptions.map((option) => (
            <option key={option.code} value={option.name}>
              {option.name}
            </option>
          ))}
        </FieldSelect>

        <FormField
          id="date"
          name="date"
          type="date"
          value={formData.operation_date}
          onChange={handleChange}
          label="日期:"
        />
        <FormField
          label="購入量(單位:包裝單位)"
          name="purchase_quantity"
          value={formData.purchase_quantity}
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
        <caption>表 8.肥料入出庫紀錄</caption>
        <thead class="table-light">
          <tr>
          <th>id</th>
          <th>資材名稱</th>
          <th>廠商</th>
          <th>供應商</th>
          <th>包裝單位</th>
          <th>包裝容量</th>
          <th>日期</th>
          <th>購入量(單位:包裝單位)</th>
          <th>使用量(單位:包裝容量)</th>
          <th>剩餘量(單位:包裝容量)</th>
          <th>備註</th>
          {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.fertilizer_material_name}</td>
              <td>{record.manufacturer || '-'}</td>
              <td>{record.supplier || '-'}</td>
              <td>{record.packaging_unit || '-'}</td>
              <td>{record.packaging_volume || '-'}</td>
              <td>{moment(record.date).format('YYYY-MM-DD')}</td>
              <td>{record.purchase_quantity || '-'}</td>
              <td>{record.usage_quantity || '-'}</td>
              <td>{record.remaining_quantity || '-'}</td>
              <td>{record.notes || '-'}</td>
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

export default Page08;

