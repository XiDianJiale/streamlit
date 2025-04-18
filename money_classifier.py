import streamlit as st
import requests
import json
import os
import base64

# 配置 OpenRouter API
API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 设置背景图片
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            opacity: 0.9;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 页面设置
st.set_page_config(page_title="智能人民币投放系统", layout="wide")

# 添加背景图片
try:
    add_bg_from_local('background.png')
except Exception as e:
    st.warning(f"背景图片加载失败: {str(e)}")

# 系统提示初始化
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = """您是一个专业的人民币投放系统助手，由启盛公司开发。
您可以帮助用户解决存钱、取钱和设备维护问题。
本系统采用颜色传感器识别不同面额的人民币，使用距离传感器检测纸币位置，并通过舵机控制投放和取钱机制。
启盛公司是一家专注于智能金融设备开发的高科技企业，这款人民币投放系统是公司的明星产品，用于便捷安全地管理现金。
当用户遇到问题时，请提供专业且友好的建议。"""

# 模拟用户数据库
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "administrator"},
        "user1": {"password": "user123", "role": "user"}
    }

# 用户登录模块
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.user_role = None

if not st.session_state.logged_in:
    st.title("用户登录")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("登录"):
            if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.user_role = st.session_state.users_db[username]["role"]
                st.success("登录成功")
                st.experimental_rerun()
            else:
                st.error("用户名或密码错误")
    with col2:
        if st.button("注册新用户"):
            if username and password:
                if username not in st.session_state.users_db:
                    st.session_state.users_db[username] = {"password": password, "role": "user"}
                    st.success("注册成功，请登录")
                else:
                    st.error("用户名已存在")
            else:
                st.error("请输入用户名和密码")
    st.stop()

# 主界面
st.sidebar.title(f"欢迎您，{st.session_state.current_user}")

# 添加用户管理模块到侧边栏
with st.sidebar.expander("用户设置"):
    if st.button("修改密码"):
        st.session_state.show_password_change = True
    if st.button("用户资料"):
        st.session_state.show_profile = True
    if st.button("退出登录"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# 根据用户角色显示不同的模式选项
if st.session_state.user_role == "administrator":
    mode = st.sidebar.selectbox("选择模式", ["操控模式", "开发者维护模式", "LLM对话", "用户管理"])
else:
    mode = st.sidebar.selectbox("选择模式", ["操控模式", "LLM对话"])

# 显示密码修改界面
if 'show_password_change' in st.session_state and st.session_state.show_password_change:
    with st.expander("密码修改", expanded=True):
        old_password = st.text_input("旧密码", type="password", key="old_pwd")
        new_password = st.text_input("新密码", type="password", key="new_pwd")
        confirm_password = st.text_input("确认新密码", type="password", key="confirm_pwd")
        
        if st.button("确认修改"):
            if st.session_state.users_db[st.session_state.current_user]["password"] == old_password:
                if new_password == confirm_password:
                    st.session_state.users_db[st.session_state.current_user]["password"] = new_password
                    st.success("密码修改成功")
                    st.session_state.show_password_change = False
                else:
                    st.error("两次输入的新密码不一致")
            else:
                st.error("旧密码不正确")

# 显示用户资料界面
if 'show_profile' in st.session_state and st.session_state.show_profile:
    with st.expander("用户资料", expanded=True):
        st.write(f"用户名: {st.session_state.current_user}")
        st.write(f"用户角色: {st.session_state.user_role}")
        if st.button("关闭"):
            st.session_state.show_profile = False

# 模拟硬件通信函数
def send_command_to_microcontroller(command):
    st.info(f"发送命令到微控制器：{command}")

def send_command_to_fpga(command):
    st.info(f"发送命令到FPGA：{command}")

# 操控模式界面
if mode == "操控模式":
    st.title("操控模式")
    option = st.radio("请选择操作：", ["开始存钱", "我要取钱", "语音指导"])
    if option == "开始存钱":
        st.info("请放入纸币")
        if st.button("确认放入"):
            send_command_to_microcontroller("识别颜色")
            send_command_to_fpga("投放纸币")
    elif option == "我要取钱":
        if st.button("确认取钱"):
            send_command_to_microcontroller("请求取钱")
            send_command_to_fpga("转动抽屉")
        if st.button("收回抽屉"):
            send_command_to_fpga("收回抽屉")
    else:
        st.audio("instruction_audio.mp3")  # 假设本地存在

# 维护模式界面 - 仅对管理员开放
elif mode == "开发者维护模式":
    st.title("维护模式")
    st.subheader("传感器与舵机控制")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("读取距离传感器"):
            send_command_to_microcontroller("读取距离")
        if st.button("读取颜色传感器"):
            send_command_to_microcontroller("读取颜色")
    with col2:
        if st.button("旋转投放舵机"):
            send_command_to_fpga("旋转投放")
        if st.button("旋转抽屉舵机"):
            send_command_to_fpga("旋转抽屉")

# 用户管理界面 - 仅对管理员开放
elif mode == "用户管理":
    st.title("用户管理")
    
    with st.expander("所有用户"):
        for user, details in st.session_state.users_db.items():
            st.write(f"用户名: {user}, 角色: {details['role']}")
    
    st.subheader("添加新用户")
    new_username = st.text_input("用户名", key="new_user")
    new_password = st.text_input("密码", type="password", key="new_pass")
    new_role = st.selectbox("角色", ["user", "administrator"])
    
    if st.button("添加"):
        if new_username and new_password:
            if new_username not in st.session_state.users_db:
                st.session_state.users_db[new_username] = {"password": new_password, "role": new_role}
                st.success(f"已添加用户 {new_username}")
            else:
                st.error("用户名已存在")
        else:
            st.error("请填写所有字段")

# LLM 对话界面
elif mode == "LLM对话":
    st.title("与智能助手对话")

    # 初始化用户特定的对话历史
    if "user_chat_histories" not in st.session_state:
        st.session_state.user_chat_histories = {}
    
    # 为当前用户获取或创建对话历史
    current_user = st.session_state.current_user
    if current_user not in st.session_state.user_chat_histories:
        st.session_state.user_chat_histories[current_user] = []
    
    # 当前用户的聊天历史
    current_chat_history = st.session_state.user_chat_histories[current_user]

    # 允许编辑系统提示（仅对管理员开放）
    if st.session_state.user_role == "administrator":
        with st.expander("编辑背景知识库"):
            st.session_state.system_prompt = st.text_area(
                "系统提示",
                st.session_state.system_prompt,
                height=200
            )

    user_input = st.text_input("你想说什么？")

    if st.button("发送") and user_input:
        with st.spinner("AI思考中..."):
            # 构建包含系统提示和历史对话的完整消息列表
            messages = [
                {"role": "system", "content": st.session_state.system_prompt}
            ]

            # 添加历史对话记录
            for history_item in current_chat_history:
                user_msg, bot_msg = history_item
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": bot_msg})

            # 添加当前用户问题
            messages.append({"role": "user", "content": user_input})

            # 发送请求
            try:
                body = {
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": messages
                }
                response = requests.post(BASE_URL + "/chat/completions", headers=headers, data=json.dumps(body))

                if response.status_code == 200:
                    reply = response.json()["choices"][0]["message"]["content"]
                else:
                    st.error(f"API错误: {response.status_code}")
                    st.error(f"错误信息: {response.text}")
                    reply = f"请求失败，状态码: {response.status_code}。请检查API配置。"
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
                reply = "连接失败，请检查网络或API配置。"

            # 将新对话添加到当前用户的历史记录
            current_chat_history.append((user_input, reply))
            st.session_state.user_chat_histories[current_user] = current_chat_history
            
            # 重新渲染页面以显示新对话
            st.experimental_rerun()

    # 分隔线
    st.divider()

    # 显示聊天历史
    st.subheader("对话历史")
    if current_chat_history:
        for user_msg, bot_msg in reversed(current_chat_history):
            st.markdown(f"**你**: {user_msg}")
            st.markdown(f"**助手**: {bot_msg}")
            st.divider()
    else:
        st.info("还没有对话，发送消息开始聊天吧！")