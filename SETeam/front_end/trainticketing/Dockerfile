# 使用 Node 作为基础镜像
FROM node:14.17.0-alpine

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json 到工作目录
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制所有文件到工作目录
COPY . .

# 构建项目
RUN npm run build

# 暴露端口（根据项目需要进行设置）
EXPOSE 8080

# 启动应用
CMD [ "npm", "run", "serve" ]
