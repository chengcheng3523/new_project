// 有害生物防治或環境消毒資材施用
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


const Page09 = () => {
  const { role, userId } = useContext(AuthContext);
  const isAdmin = role === 'admin'; 
  const [formData, setFormData] = useState({
    id: null,
    user_id: userId, 
    date_used: '',
    field_code: '',
    crop: '',
    pest_target: '',
    pest_control_material_name: '',
    water_volume: '',
    chemical_usage: '',
    dilution_factor: '',
    safety_harvest_period: '',
    operator_method: '',
    operator: '',
    notes: '',
  });

  const [validFieldCodes, setvalidFieldCodes] = useState([]);  // 儲存有效的 field_code
  const [pestcontrolOptions, setpestcontrolOptions] = useState([]);  // 儲存有效的資材名稱
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // 請求所有有效的 field_code
  const fetchValidFieldCodes = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/valid_field_codes');
      setvalidFieldCodes(response.data);  // 設置有效的 field_code
    } catch (error) {
      console.error('無法獲取有效的 field_codes:', error);
      alert('無法載入有效的田區代號，請稍後再試！');
    }
  }, []);

  // 請求所有有效的資材名稱
  const fetchPestcontrolOptions = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/pest-control-options');
      setpestcontrolOptions(response.data);  // 設置有效的資材名稱
    } catch (error) {
      console.error('無法獲取有效的資材名稱:', error);
      alert('無法載入有效的資材名稱，請稍後再試！');
    }
  }, []);

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/form09');
      console.log('原始數據:', response.data); // 打印原始數據確認結構
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item.id, // 使用 land_parcel_number 作为唯一标识符
          user_id: item.user_id,
          date_used: item.date_used,
          field_code: item.field_code,
          crop: item.crop,
          pest_target: item.pest_target,
          pest_control_material_name: item.pest_control_material_name,
          water_volume: item.water_volume,
          chemical_usage: item.chemical_usage,
          dilution_factor: item.dilution_factor,
          safety_harvest_period: item.safety_harvest_period,
          operator_method: item.operator_method,
          operator: item.operator,
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
    fetchValidFieldCodes(); // 組件加載時獲取有效的 field_code
    fetchPestcontrolOptions(); // 組件加載時獲取有效的資材名稱
    fetchData(); // 組件加載時獲取數據
  }, [fetchValidFieldCodes, fetchPestcontrolOptions, fetchData, navigate, userId]);

  const handleChange = async (e) => {

    const { name, value } = e.target;
    // 如果不是管理员并且字段是 user_id，则不更新该字段
    if (!isAdmin && name === 'user_id') {
      return;
    }

    if (name === 'field_code') {
      setFormData({
        ...formData,
        field_code: value,
        crop: '', // 清空作物選擇
      });
  
      // 根據田區代號獲取對應的作物
      if (value) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/valid_crops/${value}`);
          const crops = response.data;
  
          // 如果只有一個作物，直接填入
          if (crops.length === 1) {
            setFormData((prevFormData) => ({
              ...prevFormData,
              crop: crops[0],
            }));
          }
        } catch (error) {
          console.error('無法獲取對應的作物:', error);
          alert('無法載入對應的作物，請稍後再試！');
        }
      }
    } else {
      // 其他欄位直接更新
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

  try {
    let response;
    if (formData.id) {
      if (isAdmin) {
        response = await axios.put(`http://127.0.0.1:5000/api/form09/${formData.id}`, {
          ...formData, 
        });
      } else {
        alert('您沒有權限更新資料！');
        setLoading(false);
        return;
      }
      } else {
        // 新增資料
        response = await axios.post('http://127.0.0.1:5000/api/form09', {
          user_id: userId,
          date_used: formData.date_used,
          field_code: formData.field_code,
          crop: formData.crop,
          pest_target: formData.pest_target,
          pest_control_material_name: formData.pest_control_material_name,
          water_volume: formData.water_volume ? parseFloat(formData.water_volume) : null,
          chemical_usage: formData.chemical_usage ? parseFloat(formData.chemical_usage) : null,
          dilution_factor: formData.dilution_factor ? parseFloat(formData.dilution_factor) : null,
          safety_harvest_period: formData.safety_harvest_period ? parseInt(formData.safety_harvest_period, 10) : null,
          operator_method: formData.operator_method,
          operator: formData.operator,
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
        pest_target: '',
        pest_control_material_name: '',
        water_volume: '',
        chemical_usage: '',
        dilution_factor: '',
        safety_harvest_period: '',
        operator_method: '',
        operator: '',
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
      const response = await axios.delete(`http://127.0.0.1:5000/api/form09/${id}`);
      console.log('删除成功:', response.data);
      fetchData(); // 刷新數據
      alert('成功刪除資料！');
    } catch (error) {
      console.error('刪除請求失敗:', error.response ? error.response.data : error.message);
      alert('刪除失敗，請稍後重試！');
    }
  };


  const handleEdit = (record) => {
    if (!isAdmin) return; // 如果不是管理員，則返回

    // const isOtherUnit = !['自行育苗'].includes(record.seedling_purchase_type);
    setFormData({
      id: record.id,
      user_id: record.user_id,
      date_used: record.date_used,
      field_code: record.field_code,
      crop: record.crop,
      pest_target: record.pest_target,
      pest_control_material_name: record.pest_control_material_name,
      water_volume: record.water_volume,
      chemical_usage: record.chemical_usage,
      dilution_factor: record.dilution_factor,
      safety_harvest_period: record.safety_harvest_period,
      operator_method: record.operator_method,
      operator: record.operator,
      notes: record.notes,
    });
  };

  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
      <h4>表 9.有害生物防治或環境消毒資材施用</h4>
      <FormField
        label="使用日期"
        name="date_used"
        value={formData.date_used}
        onChange={handleChange}
        type="date"
      />

        <FieldSelect
          name="field_code"
          type="select"
          value={formData.field_code}
          onChange={handleChange}
          label="田區代號:"
          >
          <option value="">選擇田區代號</option>
          {validFieldCodes.map((fieldCode) => (
            <option key={fieldCode} value={fieldCode}>
              {fieldCode}
            </option>
          ))}
        </FieldSelect>

      <FieldSelect
        name="crop"
        type="select"
        value={formData.crop}
        onChange={handleChange}
        label="作物:"
        disabled // 這會讓 select 呈現灰底且無法互動
        >
          <option value="" disabled hidden>
            選擇作物
          </option>
          <option value={formData.crop}>{formData.crop}</option>
          </FieldSelect>

      <FormField
        label="防治對象"
        name="pest_target"
        value={formData.pest_target}
        onChange={handleChange}
        
      />

        {/* 資材名稱下拉選單 */}
        <FieldSelect
          name="pest_control_material_name"
          type="select"
          value={formData.pest_control_material_name}
          onChange={handleChange}
          label="資材代碼或名稱"
        >
          <option value="">選擇資材名稱</option>
          {pestcontrolOptions.map((option) => (
            <option key={option.code} value={option.name}>
              {option.name}
            </option>
          ))}
        </FieldSelect>

      <FormField
        label="用水量(公升)"
        name="water_volume"
        value={formData.water_volume}
        onChange={handleChange}
      />

      <FormField
        label="藥劑使用量(公斤/公升)"
        name="chemical_usage"
        value={formData.chemical_usage}
        onChange={handleChange}
      />

      <div style={{ color: 'blue', fontSize: '1em', marginBottom: '10px' }}>
        藥劑使用量(公斤/公升)，將影響入出庫計算，請務必確認資料正確無誤！
      </div>
      
      <FormField
        label="稀釋倍數"
        name="dilution_factor"
        value={formData.dilution_factor}
        onChange={handleChange}
        
      />
      <FormField
        label="安全採收期(天)"
        name="safety_harvest_period"
        value={formData.safety_harvest_period}
        onChange={handleChange}
        
      />
      <SelectField
        label="操作方式"
        name="operator_method"
        value={formData.operator_method}
        onChange={handleChange}
        
        options={[
          { value: '噴灑', label: '噴灑' },
          { value: '撒施', label: '撒施' },
          { value: '灌注', label: '灌注' },
          { value: '其他', label: '其他' }, 
        ]}
      />
      <FormField
        label="操作人員"
        name="operator"
        value={formData.operator}
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
        <caption>表 9.有害生物防治或環境消毒資材施用</caption>
        <thead class="table-light">
          <tr>
            <th>id</th>
            <th>使用日期</th>
            <th>田區代號</th>
            <th>作物</th>
            <th>防治對象</th>
            <th>資材代碼或名稱</th>
            <th>用水量(公升)</th>
            <th>藥劑使用量(公斤.公升)</th>
            <th>稀釋倍數</th>
            <th>安全採收期(天)</th>
            <th>操作方式</th>
            <th>操作人員</th>

            <th>備註</th>
            {isAdmin && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.id}</td> 
              <td>{record.date_used}</td>
              <td>{record.field_code}</td>
              <td>{record.crop}</td>
              <td>{record.pest_target}</td>
              <td>{record.pest_control_material_name}</td>
              <td>{record.water_volume}</td>
              <td>{record.chemical_usage}</td>
              <td>{record.dilution_factor}</td>
              <td>{record.safety_harvest_period}</td>
              <td>{record.operator_method}</td>
              <td>{record.operator}</td>
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


export default Page09;