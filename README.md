# Prison System

## 简介

这是一个专为监狱管理定制的内部系统，提供狱警登录、收押登记、在押名单和释放功能。

## 安装

1. 克隆仓库
```
git clone https://github.com/yourusername/prison_system.git
cd prison_system
```
2. 创建虚拟环境并安装依赖
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. 运行应用
```
export FLASK_APP=app.py
flask run
```
默认会监听 http://localhost:3000

## 默认演示账号
- 用户名: officer1
- 密码: 123456

## 项目结构
```
(prison_system目录结构参见项目根目录说明)
