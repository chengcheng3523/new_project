# 建置階段
FROM node:18-alpine AS builder

WORKDIR /app
COPY . .

# 先複製 package.json 和 package-lock.json，安裝依賴
COPY package.json package-lock.json ./
RUN npm install

# 再複製其他檔案並執行建置
COPY . .
RUN npm run build

# 部署階段
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# podman build -t frontend:V1.0.1 .
# podman run -p 3000:80 -d  frontend:V1.0.1