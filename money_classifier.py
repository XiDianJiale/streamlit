import streamlit as st
import requests
import json
import os
import base64

# API config
API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Set background
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

# CSS styling
def set_custom_style():
    st.markdown("""
        <style>
        .main-header {
            font-size: 42px;
            font-weight: bold;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 20px;
        }
        .sub-header {
            font-size: 28px;
            font-weight: bold;
            color: #1E3A8A;
        }
        .normal-text {
            font-size: 18px;
            line-height: 1.6;
        }
        .feature-card {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .team-card {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .highlight {
            color: #FF4B4B;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

# Page setup
st.set_page_config(page_title="Smart RMB Dispensing System", layout="wide")

# Add background
try:
    add_bg_from_local('background.png')
except Exception as e:
    st.warning(f"Background image failed to load: {str(e)}")

set_custom_style()

# System prompt
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = """您是一个专业的人民币投放系统助手，由启盛公司开发。
您可以帮助用户解决存钱、取钱和设备维护问题。
本系统采用颜色传感器识别不同面额的人民币，使用距离传感器检测纸币位置，并通过舵机控制投放和取钱机制。
启盛公司是一家专注于智能金融设备开发的高科技企业，这款人民币投放系统是公司的明星产品，用于便捷安全地管理现金。
当用户遇到问题时，请提供专业且友好的建议。"""

# User DB
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "administrator"},
        "user1": {"password": "user123", "role": "user"}
    }

# Login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.user_role = None

# Product promo
def show_product_promotion():
    st.markdown('<div class="main-header">智能人民币投放系统</div>', unsafe_allow_html=True)
    st.markdown('<div class="normal-text">由启盛科技倾力打造的新一代智能现金管理解决方案</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("background.png", use_column_width=True, caption="智能人民币投放系统")
    
    st.markdown('<div class="sub-header">核心亮点</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>智能识别</h3>
            <p>采用先进的颜色传感器技术，精准识别不同面额人民币，准确率高达99.9%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>安全可靠</h3>
            <p>多重验证机制，防伪技术与物理隔离设计，确保您的资金绝对安全</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>便捷操作</h3>
            <p>人性化界面设计，简单直观的操作流程，老人小孩都能轻松使用</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>智能助手</h3>
            <p>内置AI助手，随时为您解答问题，提供专业指导</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
        <h2>未来已来，智能先行</h2>
        <p style="font-size: 18px;">立即体验启盛科技带来的智能金融新时代</p>
    </div>
    """, unsafe_allow_html=True)

# Product details
def show_product_details():
    st.markdown('<div class="sub-header">产品详情</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="normal-text">
        <p>启盛智能人民币投放系统是一款专为银行、商场、社区服务站等场所设计的现金管理设备。系统集成了先进的识别技术和精密的机械控制，能够自动完成存取款、现金分类和保管等功能。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">技术规格</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>硬件规格</h3>
            <ul>
                <li>尺寸：60cm × 40cm × 150cm</li>
                <li>重量：80kg</li>
                <li>显示屏：15.6英寸触控屏</li>
                <li>电源：AC 220V, 50Hz</li>
                <li>待机功耗：<5W</li>
                <li>工作功耗：<100W</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>传感器规格</h3>
            <ul>
                <li>颜色传感器：TCS34725，RGB传感器</li>
                <li>距离传感器：VL53L0X，TOF激光测距</li>
                <li>识别精度：>99.9%</li>
                <li>处理速度：<0.5秒/张</li>
                <li>容纳能力：最多1000张</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">功能详解</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>自动识别与分类</h3>
        <p>系统采用高精度颜色传感器，能够准确识别不同面额的人民币。先进的图像处理算法能够在0.5秒内完成识别和验证，之后通过精密舵机控制将纸币分类存放。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>安全存取机制</h3>
        <p>采用双重验证机制确保交易安全。存款时，系统先验证纸币真伪，再确认存入；取款时，通过密码与生物识别双重验证，确保资金安全。所有操作都有详细记录，可追溯查询。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>智能交互系统</h3>
        <p>内置AI助手，可以语音交互，解答用户问题。系统支持多语言界面，适应不同用户需求。直观的操作流程设计，降低使用门槛，提升用户体验。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">应用场景</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3>银行网点</h3>
            <p>减轻柜员工作负担，提高服务效率</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3>商场超市</h3>
            <p>自助收银区现金处理，降低人力成本</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3>社区服务站</h3>
            <p>为居民提供24小时自助现金服务</p>
        </div>
        """, unsafe_allow_html=True)

# Team info
def show_team_info():
    st.markdown('<div class="sub-header">研发团队</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="normal-text" style="margin-bottom: 30px;">
        <p>启盛科技研发团队由西安电子科技大学的六位优秀学生组成，致力于打造最智能、最安全的金融设备。团队成员各司其职，共同推进项目顺利进行。</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="team-card">
            <h3>万子墨</h3>
            <p>上位机开发</p>
            <p>西安电子科技大学学生，负责系统上位机设计与开发</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="team-card">
            <h3>黄永兴</h3>
            <p>FPGA开发工程师</p>
            <p>西安电子科技大学学生，专注FPGA设计与实现</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="team-card">
            <h3>何家乐</h3>
            <p>微处理器(MCU)工程师</p>
            <p>西安电子科技大学学生，负责底层控制系统开发</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="team-card">
            <h3>郝家乐</h3>
            <p>网页开发工程师</p>
            <p>西安电子科技大学学生，负责Web前端设计与实现</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="team-card">
            <h3>黄宪政</h3>
            <p>机械工程师</p>
            <p>西安电子科技大学学生，负责系统机械结构设计与加工</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="team-card">
            <h3>邬宏扬</h3>
            <p>项目秘书</p>
            <p>西安电子科技大学学生，负责项目协调与文档管理</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">团队理念</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <p style="font-size: 20px; text-align: center; font-style: italic;">"科技改变金融，创新驱动未来"</p>
        <p>启盛科技团队秉持用户至上、技术创新、安全可靠的核心价值观，致力于通过技术创新解决金融行业痛点，为用户提供更便捷、更安全的金融服务体验。</p>
        <p>作为西安电子科技大学的学生团队，我们将所学知识与实际应用相结合，用年轻的视角和创新的思维，探索智能金融设备的新可能。</p>
    </div>
    """, unsafe_allow_html=True)

# Hardware simulation
def send_command_to_microcontroller(command):
    st.info(f"发送命令到微控制器：{command}")

def send_command_to_fpga(command):
    st.info(f"发送命令到FPGA：{command}")

# Operation mode
def show_operation_mode():
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
        st.audio("instruction_audio.mp3")

# Maintenance mode
def show_maintenance_mode():
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

# User management
def show_user_management():
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

# LLM chat
def show_llm_chat():
    st.title("与智能助手对话")

    if "user_chat_histories" not in st.session_state:
        st.session_state.user_chat_histories = {}
    
    current_user = st.session_state.current_user
    if current_user not in st.session_state.user_chat_histories:
        st.session_state.user_chat_histories[current_user] = []
    
    current_chat_history = st.session_state.user_chat_histories[current_user]

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
            messages = [
                {"role": "system", "content": st.session_state.system_prompt}
            ]

            for history_item in current_chat_history:
                user_msg, bot_msg = history_item
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": bot_msg})

            messages.append({"role": "user", "content": user_input})

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

            current_chat_history.append((user_input, reply))
            st.session_state.user_chat_histories[current_user] = current_chat_history
            
            st.experimental_rerun()

    st.divider()

    st.subheader("对话历史")
    if current_chat_history:
        for user_msg, bot_msg in reversed(current_chat_history):
            st.markdown(f"**你**: {user_msg}")
            st.markdown(f"**助手**: {bot_msg}")
            st.divider()
    else:
        st.info("还没有对话，发送消息开始聊天吧！")

# Password change
def show_password_change():
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

# User profile
def show_user_profile():
    with st.expander("用户资料", expanded=True):
        st.write(f"用户名: {st.session_state.current_user}")
        st.write(f"用户角色: {st.session_state.user_role}")
        if st.button("关闭"):
            st.session_state.show_profile = False

# Main app
def main():
    if not st.session_state.logged_in:
        show_product_promotion()
        
        with st.sidebar:
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
                if st.button("注册"):
                    if username and password:
                        if username not in st.session_state.users_db:
                            st.session_state.users_db[username] = {"password": password, "role": "user"}
                            st.success("注册成功，请登录")
                        else:
                            st.error("用户名已存在")
                    else:
                        st.error("请输入用户名和密码")
    else:
        st.sidebar.title(f"欢迎您，{st.session_state.current_user}")
        
        with st.sidebar.expander("用户设置"):
            if st.button("修改密码"):
                st.session_state.show_password_change = True
            if st.button("用户资料"):
                st.session_state.show_profile = True
            if st.button("退出登录"):
                st.session_state.logged_in = False
                st.experimental_rerun()
        
        if 'show_password_change' in st.session_state and st.session_state.show_password_change:
            show_password_change()
        
        if 'show_profile' in st.session_state and st.session_state.show_profile:
            show_user_profile()
        
        if st.session_state.user_role == "administrator":
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "产品宣传", "产品详情", "团队介绍", "操控模式", "维护模式", "管理功能"
            ])
            
            with tab1:
                show_product_promotion()
            
            with tab2:
                show_product_details()
            
            with tab3:
                show_team_info()
            
            with tab4:
                show_operation_mode()
            
            with tab5:
                show_maintenance_mode()
            
            with tab6:
                tab6_1, tab6_2 = st.tabs(["用户管理", "LLM对话"])
                with tab6_1:
                    show_user_management()
                with tab6_2:
                    show_llm_chat()
        else:
            tab1, tab2, tab3, tab4 = st.tabs([
                "产品宣传", "产品详情", "团队介绍", "功能"
            ])
            
            with tab1:
                show_product_promotion()
            
            with tab2:
                show_product_details()
            
            with tab3:
                show_team_info()
            
            with tab4:
                tab4_1, tab4_2 = st.tabs(["操控模式", "LLM对话"])
                with tab4_1:
                    show_operation_mode()
                with tab4_2:
                    show_llm_chat()

# Run app
if __name__ == "__main__":
    main()