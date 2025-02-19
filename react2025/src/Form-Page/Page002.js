import React, { useState , useEffect , useContext } from 'react';
import Clearfix from "../components/common/Clearfix";
// import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import moment from 'moment';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';


const Page002 = () => {
  const { role } = useContext(AuthContext); // 獲取使用者角色
  const isAdmin = role === 'admin'; // 判斷是否為管理員
  const [formData, setFormData] = useState({
    id: null,
    cultivated_crop: '',
    crop_variety: '',
    seed_source: '',
    seedling_purchase_date: '',
    seedling_purchase_type: '',
    notes: '',
  });

  const [data, setData] = useState([]); // 保存數據到狀態，定義 value 狀態
  const [loading, setLoading] = useState(false); // 控制提交按鈕的加載狀態

  // 模擬獲取數據
  const fetchData = async () => {
    try {
      // const response = await axios.get('http://localhost:5000/api/records03/get');
      const response = {
        data: [
          [1, '栽培作物', '栽培品種', '種子(苗)來源', '育苗(購入)日期','育苗(購入)種類', '備註'],
          [2, '高麗菜', '高麗菜', '自行育苗', '2025-02-17', '種子','ex：間作及敷蓋稻草'],
          [3, '高麗菜', '高麗菜', '自行育苗', '2024-11-27', '種苗','ex：間作及敷蓋稻草'],
          [4, '高麗菜', '高麗菜', '自行育苗', '1190-05-13', '繁殖體','ex：間作及敷蓋稻草'],
          [5, '高麗菜', '高麗菜', '購買來源，_______', '2025-02-18', '備註3'],
        ],
      };
      console.log(response.data); // 打印資料確認結構
      // setData(response.data);
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id:  item[0],
          cultivated_crop: item[1],
          crop_variety: item[2],
          seed_source: item[3],
          seedling_purchase_date: moment(item[4], 'YYYY-MM-DD').toDate(),
          seedling_purchase_type: item[5],
          notes: item[6],
        }));
        setData(transformedData);
      } else {
        alert('伺服器返回錯誤，請稍後重試！');
      }
    } catch (error) {
      console.error('獲取數據失敗:', error);
      alert('無法載入數據，請檢查您的伺服器或網絡連接！');
    }
  };

  useEffect(() => {
    console.log('Data to be displayed:');
    console.log('Fetching data...');
    fetchData(); // 組件加載時獲取數據
  }, []); // 空數組表示只運行一次

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
        cultivated_crop: '',
        crop_variety: '',
        seed_source: '',
        seedling_purchase_date: '',
        seedling_purchase_type: '',
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
      cultivated_crop: record.cultivated_crop,
      crop_variety: record.crop_variety,
      seed_source: record.seed_source,
      seedling_purchase_date: record.seedling_purchase_date,
      seedling_purchase_type: record.seedling_purchase_type,
      notes: record.notes,
    });
  };

  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表2.種子(苗)登記表</h4>
        <FormField
          label="栽培作物"
          name="cultivated_crop"
          value={formData.cultivated_crop}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="栽培品種"
          name="crop_variety"
          value={formData.crop_variety}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="種子(苗)來源"
          name="seed_source"
          value={formData.seed_source}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="育苗(購入)日期"
          name="seedling_purchase_date"
          type="date"
          value={formData.seedling_purchase_date}
          onChange={handleChange}
          disabled={loading}
        />
        <FormField
          label="育苗(購入)種類"
          name="seedling_purchase_type"
          type="text"
          value={formData.seedling_purchase_type}
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
        <caption>表2.種子(苗)登記表</caption>
        <thead class="table-light">
          <tr>
            <th>栽培作物</th>
            <th>栽培品種</th>
            <th>種子(苗)來源</th>
            <th>育苗(購入)日期</th>
            <th>育苗(購入)種類</th>
            <th>備註</th>
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{record.cultivated_crop}</td>
              <td>{record.crop_variety}</td>
              <td>{record.seed_source}</td>
              <td>{moment(record.seedling_purchase_date).format('YYYY-MM-DD')}</td>
              <td>{record.seedling_purchase_type}</td>
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

export default Page002;