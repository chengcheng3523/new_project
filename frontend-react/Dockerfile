# 建置階段
FROM node:18-alpine AS builder

WORKDIR /app
COPY . .

# 安裝依賴並修復 react-scripts 權限問題
RUN npm install 
RUN npm run build

# 部署階段
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]