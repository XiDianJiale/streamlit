import requests
import json

# API 配置 - 使用新提供的API密钥
API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 简单的系统提示
system_prompt = """您是一个有用的助手。"""

# 测试消息
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "你好，请简单介绍一下你自己。"}
]

# 打印请求详情
print("===== 请求详情 =====")
print(f"API密钥: {API_KEY}")
print(f"基础URL: {BASE_URL}")
print(f"请求头: {headers}")
print(f"发送消息: {messages}")

try:
    # 发送请求
    body = {
        "model": "deepseek/deepseek-prover-v2:free",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }
    print(f"\n===== 请求体 =====\n{json.dumps(body, ensure_ascii=False, indent=2)}")
    
    response = requests.post(BASE_URL + "/chat/completions", headers=headers, data=json.dumps(body))
    
    print(f"\n===== 响应状态 =====")
    print(f"状态码: {response.status_code}")
    
    # 打印完整响应
    print(f"\n===== 完整响应 =====")
    print(response.text)
    
    # 尝试解析JSON
    if response.status_code == 200:
        response_data = response.json()
        print(f"\n===== 解析后的JSON =====")
        print(json.dumps(response_data, ensure_ascii=False, indent=2))
        
        # 检查是否有choices字段
        if "choices" in response_data:
            print(f"\n===== 成功获取到回复 =====")
            reply = response_data["choices"][0]["message"]["content"]
            print(f"回复: {reply}")
        else:
            print(f"\n===== 错误: 响应中没有choices字段 =====")
            print(f"响应键: {list(response_data.keys())}")
    else:
        print(f"\n===== 错误响应 =====")
        print(f"错误详情: {response.text}")
        
except Exception as e:
    print(f"\n===== 异常捕获 =====")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {str(e)}")
    import traceback
    print(f"错误堆栈: {traceback.format_exc()}")

# 测试使用完整URL格式
try:
    print("\n\n===== 尝试使用完整URL格式 =====")
    full_url = "https://openrouter.ai/api/v1/chat/completions"
    print(f"完整URL: {full_url}")
    
    full_response = requests.post(full_url, headers=headers, data=json.dumps(body))
    
    print(f"\n===== 完整URL响应状态 =====")
    print(f"状态码: {full_response.status_code}")
    
    # 打印完整响应
    print(f"\n===== 完整URL响应内容 =====")
    print(full_response.text)
    
    if full_response.status_code == 200:
        full_data = full_response.json()
        if "choices" in full_data:
            print(f"\n===== 完整URL成功获取到回复 =====")
            full_reply = full_data["choices"][0]["message"]["content"]
            print(f"回复: {full_reply}")
    
except Exception as e:
    print(f"\n===== 完整URL异常捕获 =====")
    print(f"错误信息: {str(e)}")

# 测试使用其他请求参数
try:
    print("\n\n===== 尝试使用其他请求参数 =====")
    params_body = {
        "model": "deepseek/deepseek-prover-v2:free",
        "messages": messages,
        "temperature": 0.5,  # 更低的温度值
        "max_tokens": 300,   # 限制回复长度
        "stream": False      # 确保不使用流式响应
    }
    print(f"\n===== 参数请求体 =====\n{json.dumps(params_body, ensure_ascii=False, indent=2)}")
    
    params_response = requests.post(BASE_URL + "/chat/completions", headers=headers, data=json.dumps(params_body))
    
    print(f"\n===== 参数响应状态 =====")
    print(f"状态码: {params_response.status_code}")
    
    # 打印完整响应
    print(f"\n===== 参数响应内容 =====")
    print(params_response.text)
    
    if params_response.status_code == 200:
        params_data = params_response.json()
        if "choices" in params_data:
            print(f"\n===== 参数成功获取到回复 =====")
            params_reply = params_data["choices"][0]["message"]["content"]
            print(f"回复: {params_reply}")
    
except Exception as e:
    print(f"\n===== 参数异常捕获 =====")
    print(f"错误信息: {str(e)}")
