import os
import requests

# 强烈建议将API Key设置为环境变量，而不是硬编码在代码里
# 在你的终端中执行: export MOONSHOT_API_KEY='你的API Key'
API_KEY = os.getenv("MOONSHOT_API_KEY")
API_URL = "https://api.moonshot.cn/v1/chat/completions"

def generate_scenario_analysis(mbti_a, mbti_b, scenario):
    """
    调用大模型API，生成CP剧情模拟分析。
    """
    if not API_KEY:
        return "错误：请先设置 MOONSHOT_API_KEY 环境变量"

    # 这就是魔法的核心：Prompt Engineering！
    system_prompt = f"""
你是一位精通MBTI性格分析和人际关系心理学的“CP剧情模拟器”。
你的任务是基于用户提供的两个MBTI人格类型和一个具体情景，进行一场深刻、有趣且富有洞察力的推演。

【重要指令】
1.  你的所有输出内容，从键名到键值，都必须严格使用【简体中文】。
2.  你的输出必须严格、清晰地遵循下面的JSON格式，不要有任何多余的解释和开场白。

【JSON输出格式示例】
{{
  "标题": "INFJ 与 ENFP 的计划与随性之争",
  "人格分析": {{
    "人格A": {{
      "类型": "INFJ (引路人)",
      "核心特质": ["理想主义", "深思熟虑", "共情", "寻求意义"]
    }},
    "人格B": {{
      "类型": "ENFP (追梦人)",
      "核心特质": ["热情洋溢", "创意无限", "适应性强", "以人为本"]
    }}
  }},
  "情景剧本": [
    {{
      "步骤标题": "第一幕：矛盾的起点",
      "内容": "当需要为周末做计划时，INFJ可能已经默默构思好了一个详细、富有意义的行程。而ENFP可能会突然提出一个天马行空的新主意，打乱了原有的节奏。"
    }},
    {{
      "步骤标题": "第二幕：内心戏大公开",
      "内容": "INFJ的内心OS：'我的计划被打乱了，感觉不被尊重，而且充满了不确定性，好焦虑。' ENFP的内心OS：'哇，新主意好酷！为什么不试试呢？计划那么死板多无聊啊！'"
    }},
    {{
      "步骤标题": "第三幕：高情商对话建议",
      "内容": "INFJ可以尝试说：'你提的这个想法听起来很有趣！我们能不能把它融入到某个时间段，或者作为备选方案？我只是需要一个大致的框架来让我感到安心。' ENFP可以回应：'当然！我完全理解你需要计划！那我们先定下2个必去的地方，剩下的时间就自由探索，怎么样？'"
    }},
    {{
      "步骤标题": "第四幕：关系升华",
      "内容": "通过这样的沟通，INFJ学会了在框架内拥抱变化，而ENFP也学会了尊重伴侣的安全感。双方都向对方的世界迈出了一小步。"
    }}
  ],
  "锦囊妙计": "给这对CP的一个小建议：设立一个“惊喜时间盒子”，在计划中明确留出一段完全自由、可以由ENFP主导的随性探索时间。"
}}
"""

    user_prompt = f"""
    请为以下CP组合和情景进行推演：
    - 人格A: {mbti_a}
    - 人格B: {mbti_b}
    - 模拟情景: "{scenario}"

    请生成推演结果。
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 我们要求模型返回JSON对象，这样前端处理起来最方便
    payload = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "response_format": { "type": "json_object" } 
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()  # 如果请求失败则抛出异常

        # 解析返回的JSON，并提取内容
        json_response = response.json()
        analysis_content = json_response['choices'][0]['message']['content']

        return analysis_content

    except requests.exceptions.RequestException as e:
        return f"错误：API请求失败 - {e}"

# --- 本地测试 ---
if __name__ == "__main__":
    print("--- 正在进行本地测试 ---")

    test_mbti_a = "INFJ"
    test_mbti_b = "ENFP"
    test_scenario = "我们因为“计划 vs. 随性”吵架了，怎么办？"

    print(f"测试输入：\n人格A: {test_mbti_a}\n人格B: {test_mbti_b}\n情景: {test_scenario}\n")

    result = generate_scenario_analysis(test_mbti_a, test_mbti_b, test_scenario)

    print("--- AI生成结果 ---")
    print(result)