// 肥料入出庫
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
import moment from 'moment';


const Page08 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    material_name: '',
    manufacturer: '',
    supplier : '',
    date: '',
    packaging_unit : '',
    packaging_unit_other: '', // 新增：當選擇「其他」時的單位輸入
    volumeValue: '',          // 新增：包裝容量的數字部分
    volumeUnit: '',           // 新增：包裝容量的單位部分
    volumeUnit_other: '',     // 新增：當選擇「其他」時的單位輸入
    packaging_volume : '',
    purchase_quantity : '',
    usage_quantity : '',
    remaining_quantity : '',
    notes: '',
  });

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form08');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, // 使用 land_parcel_number 作为唯一标识符
          user_id: item.user_id,
          material_name: item.material_name,
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
      setFormData(prev => ({ ...prev, user_id: userId })); // 動態更新 user_id 
      fetchData(); // 組件加載時獲取數據
    }, [fetchData, navigate, userId]);
  
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

      // 自動更新包裝容量
      if (name === 'volumeValue' || name === 'volumeUnit' || name === 'volumeUnit_other') {
        const packagingVolume = `${newFormData.volumeValue} ${newFormData.volumeUnit === '其他' ? newFormData.volumeUnit_other : newFormData.volumeUnit}`;
        newFormData.packaging_volume = packagingVolume;
      }

      setFormData(newFormData);
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
  

    // 驗證使用量和剩餘量不超過購入量
    const purchase = parseFloat(formData.purchase_quantity);
    const usage = parseFloat(formData.usage_quantity) || 0;
    const remaining = parseFloat(formData.remaining_quantity) || 0;
    if (usage > purchase) {
      alert('使用量不能大於購入量！');
      setLoading(false);
      return;
    }
    if (remaining > purchase) {
      alert('剩餘量不能大於購入量！');
      setLoading(false);
      return;
    }

  // 合併包裝容量
  // const packaging_volume = `${formData.volumeValue} ${formData.volumeUnit}`;
  const packaging_unit = formData.packaging_unit === '其他' ? formData.packaging_unit_other : formData.packaging_unit;
  const packaging_volume = `${formData.volumeValue} ${formData.volumeUnit === '其他' ? formData.volumeUnit_other : formData.volumeUnit}`;

  try {
    let response;
    if (formData.id) {
      if (isAdmin) {
        response = await axios.put(`http://127.0.0.1:5000/api/form08/${formData.id}`, {
          ...formData,
          packaging_volume,
          packaging_unit,
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
          material_name: formData.material_name,
          manufacturer: formData.manufacturer,
          supplier: formData.supplier,
          date: formData.date,
          packaging_unit,
          packaging_volume, 
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
        material_name: '',
        manufacturer: '',
        supplier: '',
        date: '',
        packaging_unit: '',
        packaging_unit_other: '',
        volumeValue: '',
        volumeUnit: '',
        volumeUnit_other: '',
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
    
    // 分解 packaging_volume 為數字和單位
    const [volumeValue, volumeUnit] = record.packaging_volume ? record.packaging_volume.split(' ') : ['', ''];
    const isOtherPackagingUnit = !['包', '瓶', '罐'].includes(record.packaging_unit);
    const isOtherVolumeUnit = !['公克', '公斤', '毫升', '公升'].includes(volumeUnit);
  
    setFormData({
      id: record.id,
      user_id: record.user_id,
      material_name: record.material_name || '',
      manufacturer: record.manufacturer || '',
      supplier: record.supplier || '',
      date: record.date || '',
      packaging_unit: isOtherPackagingUnit ? '其他' : record.packaging_unit || '',
      packaging_unit_other: isOtherPackagingUnit ? record.packaging_unit : '',
      volumeValue: volumeValue || '',
      volumeUnit: isOtherVolumeUnit ? '其他' : volumeUnit || '',
      volumeUnit_other: isOtherVolumeUnit ? volumeUnit : '',
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
        <FormField
          label="資材名稱"
          name="material_name"
          value={formData.material_name}
          onChange={handleChange}
        />
        <FormField
          label="廠商"
          name="manufacturer"
          value={formData.manufacturer}
          onChange={handleChange}
        />
        <FormField
          label="供應商"
          name="supplier"
          value={formData.supplier}
          onChange={handleChange}
        />
        <SelectField
          label="包裝單位"
          name="packaging_unit"
          value={formData.packaging_unit}
          onChange={handleChange}
          
          options={[
            { label: '包', value: '包' },
            { label: '瓶', value: '瓶' },
            { label: '罐', value: '罐' },
            { label: '其他', value: '其他' },
          ]}

        />
        {formData.packaging_unit === '其他' && (
          <FormField
            label="包裝單位 (其他)"
            name="packaging_unit_other"
            value={formData.packaging_unit_other}
            onChange={handleChange}
            
          />
        )}
        <FormField
          label="包裝容量 (數字)"
          name="volumeValue"
          type="number"
          value={formData.volumeValue}
          onChange={handleChange}
          
        />
        <SelectField
          label="包裝容量 (單位)"
          name="volumeUnit"
          value={formData.volumeUnit}
          onChange={handleChange}
          
          options={[
            { label: '公克', value: '公克' },
            { label: '公斤', value: '公斤' },
            { label: '毫升', value: '毫升' },
            { label: '公升', value: '公升' },
            { label: '其他', value: '其他' },
          ]}
        />
        {formData.volumeUnit === '其他' && (
          <FormField
          label="包裝容量 (其他)"
          name="volumeUnit_other"
          value={formData.volumeUnit_other}
          onChange={handleChange}
          
        />
      )}
        <FormField
          id="date"
          name="date"
          type="date"
          value={formData.operation_date}
          onChange={handleChange}
          label="日期:"
        />
        <FormField
          label="購入量"
          name="purchase_quantity"
          value={formData.purchase_quantity}
          onChange={handleChange}
        />
        <FormField
          label="使用量"
          name="usage_quantity"
          value={formData.usage_quantity}
          onChange={handleChange}
        />
        <FormField
          label="剩餘量"
          name="remaining_quantity"
          value={formData.remaining_quantity}
          onChange={handleChange}
          // disabled // 禁用手動輸入，改為自動計算
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
          <th>購入量</th>
          <th>使用量</th>
          <th>剩餘量</th>
          <th>備註</th>
          {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td>
              <td>{record.material_name}</td>
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
      <Clearfix height="500px" />
    </div>
  );
};

export default Page08;


// 表單問題一，【包裝容量】在資料庫可填入的是 數字 ，後面需要加上 單位 作法，包裝容量分離數字和單位，並且單位有選項是【其他】，需要填入 (單位) 字串 
// 表單問題二，使用量和剩餘量的數字應該是要小於購入量，如何設定?
// 表單問題三，自動計算剩餘量，如何設定?
// 表單問題四，修改時，選項並未返回表單，這是錯誤的，如何修正?
// 表單問題五，需要確認【包裝單位】在資料庫可選【其他】需填入 (單位) 字串?並且在修改時需要可返回選項和輸入框與其他相同，需要調整