# AI FastAPI 101

一个用于练习 FastAPI、Pydantic、异步模型调用和自动测试的最小项目。

## 功能

- `GET /health`：检查服务是否运行
- `POST /chat`：通过 OpenRouter 调用模型并返回文本回答
- `/docs`：FastAPI 自动生成的 Swagger 交互文档

## 项目结构

- `main.py`：FastAPI 应用、数据模型和 endpoints
- `test_main.py`：接口自动测试
- `requirements.txt`：运行依赖
- `requirements-dev.txt`：测试依赖

## 安装与运行

创建并激活虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

安装依赖：

```bash
python -m pip install -r requirements-dev.txt
```

在当前终端会话中安全设置 OpenRouter Key：

```bash
read -s "OPENROUTER_API_KEY?OpenRouter API key: "
export OPENROUTER_API_KEY
echo
```

启动服务：

```bash
python -m uvicorn main:app --reload
```

启动后访问：

- Swagger 文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/health`

## 测试

运行：

```bash
python -m pytest -v
```

测试覆盖：

- `/health` 正常返回
- `/chat` 缺少必填字段时返回 `422`
- `/chat` 使用 mock 模型响应时返回结构化结果

测试中的模型调用使用 `AsyncMock` 替代，不访问 OpenRouter，也不会产生 API 费用。

## 同步与异步选择

`/health` 使用普通 `def`，因为它只返回固定数据，没有网络等待。

`/chat` 使用 `async def`，因为它需要等待 OpenRouter 的网络响应。`await` 会在等待期间把控制权交还事件循环，使同一个 worker 可以处理其他请求。

异步提高的是 I/O 等待期间的并发处理能力，不会自动加速 CPU 密集型计算。
