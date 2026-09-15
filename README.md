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
- 查询不存在任务时返回 404
- 创建任务并查询
- 更新任务完成状态
- 删除任务

运行测试

```bash
  python -m pytest -q
```

## Docker 运行与数据持久化

以下命令在项目根目录的 PowerShell 中执行，需要先启动 Docker Desktop。

### 1. 构建镜像

```powershell
docker build -t task-manager-api:latest .
```

### 2. 使用命名 volume 启动容器

```powershell
docker run -d --name task-manager-persist-1 -p 8001:8000 --mount source=task-manager-data,target=/data -e DATABASE_URL=sqlite:////data/tasks.db task-manager-api:latest
```

打开接口文档：http://localhost:8001/docs

- `task-manager-data` 是命名 volume，首次使用时自动创建。
- volume 挂载到容器内的 `/data` 目录。
- `DATABASE_URL` 指定 SQLite 数据库文件为 `/data/tasks.db`。
- 未设置 `DATABASE_URL` 时，默认使用 `sqlite:///tasks.db`。

### 3. 验证数据持久化

通过接口文档中的 `POST /tasks` 创建任务，标题设置为 `volume-persistence-test`，记录返回的 `id`。

停止并删除旧容器：

```powershell
docker stop task-manager-persist-1
docker rm task-manager-persist-1
```

使用同一个 volume 启动新容器：

```powershell
docker run -d --name task-manager-persist-2 -p 8001:8000 --mount source=task-manager-data,target=/data -e DATABASE_URL=sqlite:////data/tasks.db task-manager-api:latest
```

查询原任务（将 `1` 替换为实际返回的任务 ID）：

```powershell
curl.exe http://localhost:8001/tasks/1
```

如果仍能查询到原任务，说明数据在删除并重建容器后成功保留。

删除容器不会删除这里使用的命名 volume；保留数据需要保留 `task-manager-data`。

## 使用 Docker Compose

前提：Docker Desktop 已启动，已有命名 volume `task-manager-data`，且本机 8001 端口空闲。

构建镜像并在后台启动：

```powershell
docker compose up -d --build
```

访问 API 文档：http://localhost:8001/docs

Compose 使用外部 volume `task-manager-data`，将其挂载到容器的 `/data`，数据库路径为 `/data/tasks.db`。
