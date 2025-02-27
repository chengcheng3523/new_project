import React, { useState , useEffect , useContext, useCallback  } from 'react';
import Clearfix from "../components/common/Clearfix";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import moment from 'moment';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';


const Page02 = () => {
  const { role, filterDataByRole ,userId } = useContext(AuthContext);
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

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false); 

  // 模擬獲取數據
  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/records03/get');
      console.log('原始數據:', response.data); // 打印資料確認結構
      // setData(response.data);
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item[0],
          user_id: item[1],
          area_code: item[2],
          area_size: item[3],
          month: item[4],
          crop_info: item[5],
          notes: item[6],
        }));        
        const filteredData = filterDataByRole(transformedData);
        setData(filteredData);
      } else {
        alert('伺服器返回錯誤，請稍後重試！');
      }
    } catch (error) {
      console.error('獲取數據失敗:', error);
      alert('無法載入數據，請檢查您的伺服器或網絡連接！');
    }
  }, [filterDataByRole, userId]);

  useEffect(() => {
    console.log('Data to be displayed:');
    console.log('Fetching data...');
    fetchData(); // 組件加載時獲取數據
  }, [fetchData]); // 包含 fetchData 作為依賴項

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // 開啟加載狀態
    try {
      // 格式化日期為 MySQL 支持的格式
      if (formData.OperationDate) {
        formData.OperationDate = moment(formData.OperationDate).format('YYYY-MM-DD HH:mm:ss');
      }
      // const response = await axios.post('http://localhost:5000/api/records03/post', formData);
      let response;
      if (formData.id) {
        // 更新現有資料
        response = {
          data: data.map(item => item.id === formData.id ? { ...formData, id: item.id } : item),
        };
      } else {
        // 新增資料
        response = {
          data: [
            ...data,
            {
              id: data.length + 1,
              ...formData,
            },
          ],
        };
      }
      setData(response.data); // 更新表格數據
      setFormData({
        id: null,
        user_id: userId, // 新增 user_id
        area_code: '',
        area_size: '',
        month: '',
        crop_info: '',
        notes: '',
      }); // 清空表單
      alert('成功儲存資料！'); // 成功提示
      console.log('成功發送請求，回應:', response.data);
    } catch (error) {
      console.error('發送請求失敗:', error);
      alert('儲存失敗，請稍後重試！'); // 錯誤提示
    } finally {
      setLoading(false); // 關閉加載狀態
    }
  };

  const handleDelete = async (id) => {
    if (!isAdmin) return; // 如果不是管理員，則返回
    try {
      // const response = await axios.delete(`http://localhost:5000/api/records03/delete/${id}`);
      const response = {
        data: data.filter(record => record.id !== id),
      };
      setData(response.data); // 更新表格數據
      alert('成功刪除資料！'); // 成功提示
      console.log('成功刪除資料，回應:', response.data);
    } catch (error) {
      console.error('刪除請求失敗:', error);
      alert('刪除失敗，請稍後重試！'); // 錯誤提示
    }
  };

  const handleEdit = (record) => {
    if (!isAdmin) return; // 如果不是管理員，則返回
    setFormData({
      id: record.id,
      user_id: record.user_id, // 新增 user_id
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
        <FormField
          label="場區代號"
          name="area_code"
          value={formData.area_code}
          onChange={handleChange}
          required
          disabled={loading}
        />
        <FormField
          label="場區面積"
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
      <table className="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>場區代號</th>
            <th>場區面積</th>
            <th>月份</th>
            <th>種植作物種類、產期、預估產量(公斤)ex：小白菜/1000</th>
            <th>備註</th>
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.area_code}</td>
              <td>{record.area_size}</td>
              <td>{record.month}</td>
              <td>{record.crop_info}</td>
              <td>{record.notes}</td>
              {isAdmin && (
                <td>
                <EditButton className="btn btn-warning btn-sm" onClick={() => handleEdit(record)}>更正</EditButton>
                <DeleteButton className="btn btn-danger btn-sm" onClick={() => handleDelete(record.id)}>刪除</DeleteButton>
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