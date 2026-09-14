# Task Manager API

## 项目简介

基于 FastAPI 开发任务管理 RESTful API，使用 SQLModel 与 SQLite 实现数据持久化；完成任务创建、列表查询、按 ID 查询、状态更新和删除等 CRUD 功能，并通过 HTTPException 实现资源不存在时的 404 异常处理；使用 Swagger 完成接口联调与功能验证。

## 技术栈

- Python 3.13
- FastAPI
- SQLModel
- SQLite
- Uvicorn


## 已实现功能

- 创建任务
- 查询全部任务
- 根据ID查询任务
- 标记任务为已完成
- 删除任务
- 任务不存在时返回404


## API接口

| Method | Path | Description |
| --- | --- | ---|
| POST | /tasks | 创建任务 |
| GET | /tasks | 获取全部任务 |
| GET | /tasks/{task_id} | 获取单个任务 |
| PATCH | /tasks/{task_id}/complete | 标记任务完成 |
| DELETE | /tasks/{task_id} | 删除任务 |


## 本地运行
### 1.创建虚拟环境
```bash
  python -m venv .venv
```
### 2.激活虚拟环境
```bash
  .\.venv\Scripts\Activate.ps1
```
### 3.安装项目依赖
```bash
  pip install -r requirements.txt
```
### 4.启动服务
```bash
  uvicorn main:app --reload
```
### 5.打开API文档
```bash
  http://127.0.0.1:8000/docs
```


## 自动化测试

项目使用 pytest 和 FastAPI TestClient 进行接口自动化测试

测试使用独立的内存 SQLite 数据库，与本地开发数据库隔离

当前覆盖：
- 查询不存任务时返回 404
- 创建任务并查询
- 更新任务完成状态
- 删除任务

运行测试

```bash
  python -m pytest -q
```

