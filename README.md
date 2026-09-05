# Startinal Product Motion Forge

一个面向 TikTok Shop 商品视频矩阵的本地优先基础工程。它把原始素材、产品事实、成片复盘和投放结论分开保存；创作任务只检索当前产品最相关的内容，而不是每次读取整个素材文件夹。

## 当前能力

- 按产品扫描素材文件夹，记录路径、文件大小、SHA-256 指纹和素材类型；重复文件不会重复入库。
- 保存可审计的运营记忆：产品事实、创意规律、素材标签、合规规则和复盘结论。
- 使用 SQLite FTS 全文检索，为后续 RAG 提供本地验证版本。
- 所有记录包含产品 ID 和证据字段，避免把没有数据支持的推测当作长期规律。

## 快速开始

使用 Codex 附带的 Python 3.12：

```powershell
$python = 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
${env:PYTHONPATH} = 'src'
& $python -m ai_video_factory init --db .\data\factory.db
& $python -m ai_video_factory ingest --db .\data\factory.db --product toy-001 --source C:\素材\toy-001
& $python -m ai_video_factory remember --db .\data\factory.db --product toy-001 --kind product_fact --content 'The product is a magnetic building toy for ages 3+.' --evidence 'product specification v1' --status approved
& $python -m ai_video_factory retrieve --db .\data\factory.db --product toy-001 --query 'UGC unboxing hook CTA'
```

## 新同事验收

克隆或解压项目后，在项目根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_team_checkout.ps1
```

脚本只检查项目 Skill、Python、Node、FFmpeg、本机 `.env` 是否存在、前后端依赖和 Git 提交身份；不会读取密钥值、安装软件、启动服务或调用即梦。完整操作见 [同事使用说明](skills/startinal-jimeng-short-video-production/同事使用说明.md)。

运行测试：

```powershell
${env:PYTHONPATH} = 'src'
& $python -m unittest discover -s tests -v
```

## 推荐素材目录

```text
products/
  toy-001/
    product-images/
    real-footage/
      unboxing/
      handheld/
      play-demo/
    brand-rules/
    performance-data/
```

## 云端迁移路线

本地 SQLite 和文件夹只用于起步验证。正式跨电脑协作时：原始素材迁移至 S3 兼容对象存储，数据库迁移至 PostgreSQL + pgvector；保留本项目的产品 ID、资产 SHA-256 和记忆记录即可。API Key 只放在部署环境，不写进数据库或仓库。

## 生产能力边界

- 项目已包含 JiMeng 图生视频任务运行器、断点恢复、短期下载链接刷新、衔接帧抽取及 FFmpeg 本地拼接；所有付费提交仍必须经人工明确批准。
- 已接入的是本地生产辅助能力，不是无人值守的自动投放系统。商品事实、合规限制、付费生成和成片验收仍需人工确认。
- 语音、自动发布、TikTok 数据导入与跨电脑共享数据库尚未接入；当前跨电脑协作以版本化项目、各自本机 `.env` 和素材库清单为准。

## Startinal 商品视频工坊 MVP

当前已加入前后端分离的本地优先工作台：

- `backend/`：FastAPI、SQLite、账号角色、产品资料、生产包和管理员审核接口。
- `frontend/`：React/Vite 可视化界面；素材仍保存在用户电脑登记的本地文件夹，主机只保存资料与审核状态。
- 默认角色：首次打开时创建管理员；管理员可审核生产包，普通用户只能管理自己的产品。

启动后端（PowerShell）：

```powershell
& '.\.venv\Scripts\python.exe' -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

启动前端：

```powershell
Set-Location frontend
& 'C:\Program Files\nodejs\npm.cmd' run dev
```

浏览器打开 `http://127.0.0.1:5173/`。首次访问会创建管理员账号。当前生成的是内容生产包草稿，不会调用即梦 API。
