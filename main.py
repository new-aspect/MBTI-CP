# main.api.py (最终部署版)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # 1. 导入StaticFiles
from fastapi.responses import FileResponse # 2. 导入FileResponse
from pydantic import BaseModel
import uvicorn

from main_logic import generate_scenario_analysis

app = FastAPI(title="CP剧情模拟器 API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    mbti_a: str
    mbti_b: str
    scenario: str

@app.post("/analyze")
async def analyze_scenario(request: AnalysisRequest):

    # (先将我们原来的代码注释掉)
    result_str = generate_scenario_analysis(
        request.mbti_a,
        request.mbti_b,
        request.scenario
    )
    # 我们直接返回解析后的JSON对象，而不是一个JSON字符串
    import json
    try:
        # 尝试将结果字符串解析为JSON对象
        return json.loads(result_str)
    except json.JSONDecodeError:
        # 如果解析失败，返回一个错误提示
        return {"error": "AI返回的结果不是有效的JSON格式", "raw_result": result_str}


# 3. 让 FastAPI 托管静态文件 (我们的前端)
# 我们创建一个名为 "static" 的文件夹来存放前端文件
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    # 4. 当用户访问根路径 (/) 时，返回 index.html
    return FileResponse('static/index.html')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)