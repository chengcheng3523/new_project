import React, { useState , useEffect , useContext } from 'react';
import Clearfix from "../components/common/Clearfix";
// import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from '../components/auth/AuthContext';
import FormField from '../components/common/FormField';
import moment from 'moment';
import Form from '../components/common/Form';
import { Button, DeleteButton, EditButton } from '../components/common/Button';


const Page003 = () => {
  const { role } = useContext(AuthContext); // 獲取使用者角色
  const isAdmin = role === 'admin'; // 判斷是否為管理員
  const [formData, setFormData] = useState({
    OperationDate: '',
    FieldCode: '',
    Crop: '',
    CropContent: '',
    WorkItemCode: '',
  });
  
  const [data, setData] = useState([]); // 保存數據到狀態，定義 value 狀態
  const [loading, setLoading] = useState(false); // 控制提交按鈕的加載狀態

  // 模擬獲取數據
  const fetchData = async () => {
    try {
      // const response = await axios.get('http://localhost:5000/api/records03/get');
      const response = {
        data: [
          [1, '2025-02-17', 'A01', '稻米', '(1-1) 整地', '備註1'],
          [2, '2025-02-18', 'A02', '小麥', '(1-2) 作畦', '備註2'],
        ],
      };
      console.log(response.data); // 打印資料確認結構
      // setData(response.data);
      if (Array.isArray(response.data)) {
        const transformedData = response.data.map(item => ({
          id: item[0],
          OperationDate: item[1],
          FieldCode: item[2],
          Crop: item[3],
          CropContent: item[4],
          WorkItemCode: item[5]
        }));
        setData(transformedData);
      } else {
        alert('伺服器返回錯誤，請稍後重試！');
      }
      // console.log('Transformed data:', transformedData); // 確認轉換後的數據 
      // setData(transformedData); // 更新狀態
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
        OperationDate: '',
        FieldCode: '',
        Crop: '',
        CropContent: '',
        WorkItemCode: '',
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
      OperationDate: moment(record.OperationDate).format('YYYY-MM-DD'),
      FieldCode: record.FieldCode,
      Crop: record.Crop,
      CropContent: record.CropContent,
      WorkItemCode: record.WorkItemCode,
    });
  };

  return (
    <div className="container">
      <Clearfix height="100px" />
      <Form onSubmit={handleSubmit}>
        <h4>表3.栽培工作紀錄</h4>
        <FormField
          id="OperationDate"
          name="OperationDate"
          type="date"
          value={formData.OperationDate}
          onChange={handleChange}
          label="作業日期:"
        />
        <FormField
          id="FieldCode"
          name="FieldCode"
          type="text"
          value={formData.FieldCode}
          onChange={handleChange}
          label="田區代號:"
        />
        <FormField
          id="Crop"
          name="Crop"
          type="text"
          value={formData.Crop}
          onChange={handleChange}
          label="作物:"
        />
        <div className="mb-3">
          <label htmlFor="CropContent" className="form-label">作業內容(可填寫代碼):</label>
          <select
            className="form-select"
            id="CropContent"
            name="CropContent"
            value={formData.CropContent}
            onChange={handleChange}
            required
          >
            <option value="(1-1) 整地">(1-1) 整地</option>
            <option value="(1-2) 作畦">(1-2) 作畦</option>
            <option value="(1-3) 配置灌溉/澆水管線">(1-3) 配置灌溉/澆水管線</option>
            <option value="(1-4) 土壤改良">(1-4) 土壤改良</option>
            <option value="(1-5) 土壤消毒">(1-5) 土壤消毒</option>
            <option value="(1-6) 設施操作">(1-6) 設施操作</option>
            <option value="(1-8) 遮蔭網">(1-8) 遮蔭網</option>
            <option value="(2-1) 介質消毒">(2-1) 介質消毒</option>
            <option value="(2-2) 裝袋作業">(2-2) 裝袋作業</option>
            <option value="(2-3) 上架">(2-3) 上架</option>
            <option value="(2-4) 介質調配">(2-4) 介質調配</option>
            <option value="(2-5) 養液配置">(2-5) 養液配置</option>
            <option value="(3-1) 播種">(3-1) 播種</option>
            <option value="(3-2) 育苗">(3-2) 育苗</option>
            <option value="(3-3) 定植(移植)">(3-3) 定植(移植)</option>
            <option value="(3-4) 播種前種子處理">(3-4) 播種前種子處理</option>
            <option value="(4-1) 中耕">(4-1) 中耕</option>
            <option value="(4-2) 灌溉/澆水">(4-2) 灌溉/澆水</option>
            <option value="(4-3) 培土">(4-3) 培土</option>
            <option value="(4-4) 摘葉">(4-4) 摘葉</option>
            <option value="(4-5) 缺株補植">(4-5) 缺株補植</option>
            <option value="(4-6) 整蔓">(4-6) 整蔓</option>
            <option value="(4-7) 授粉">(4-7) 授粉</option>
            <option value="(4-8) 套袋">(4-8) 套袋</option>
            <option value="(4-9) 立支柱">(4-9) 立支柱</option>
            <option value="(5-1) 基肥">(5-1) 基肥</option>
            <option value="(5-2) 追肥">(5-2) 追肥</option>
            <option value="(5-3) 液肥">(5-3) 液肥</option>
            <option value="(6-1) 施用防治資材">(6-1) 施用防治資材</option>
            <option value="(6-2) 栽培防治">(6-2) 栽培防治</option>
            <option value="(6-3) 物理防治">(6-3) 物理防治</option>
            <option value="(6-4) 生物防治">(6-4) 生物防治</option>
            <option value="(6-5) 忌避作物">(6-5) 忌避作物</option>
            <option value="(6-6) 人工除草">(6-6) 人工除草</option>
            <option value="(6-7) 覆蓋">(6-7) 覆蓋</option>
            <option value="(6-8) 機械中耕">(6-8) 機械中耕</option>
            <option value="(7-1) 採收">(7-1) 採收</option>
            <option value="(7-2) 產季結束">(7-2) 產季結束</option>
            <option value="8. 其他">8. 其他</option>
          </select>
        </div>
        <FormField
          id="WorkItemCode"
          name="WorkItemCode"
          type="textarea"
          value={formData.WorkItemCode}
          onChange={handleChange}
          label="備註作業內容：(選填)"
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
            <th>作業日期</th>
            <th>田區代號</th>
            <th>作物</th>
            <th>作業內容</th>
            <th>備註</th>
          </tr>
        </thead>
        <tbody>
          {data.map((record) => (
            <tr key={record.id || record.FieldCode}>
              <td>{moment(record.OperationDate).format('YYYY-MM-DD')}</td>
              <td>{record.FieldCode}</td>
              <td>{record.Crop}</td>
              <td>{record.CropContent}</td>
              <td>{record.WorkItemCode}</td>
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

export default Page003;