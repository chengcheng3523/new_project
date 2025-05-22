# 前端 Dockerfile 

# 建置階段
FROM node:18-alpine3.19 AS builder

WORKDIR /app


# 先複製 package.json 和 package-lock.json，安裝依賴
COPY package.json package-lock.json ./
RUN npm install

# 再複製其他所有檔案（不包含 node_modules）
COPY . .

# 明確給予 react-scripts 執行權限
RUN chmod +x ./node_modules/.bin/react-scripts

RUN npm run build

# 部署階段
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


# cd frontend-react
# React 前端映像檔 
# podman build -t frontend:V1.0.1 .

# 建置完成後你會看到類似這樣的輸出結尾：
# Successfully tagged localhost/frontend:V1.0.1

# 指令啟動前端容器
# podman run -p 3000:80 -d  frontend:V1.0.1
# 開瀏覽器訪問
# http://localhost:3000