import streamlit as st
import requests #requirements
import json
import os
import base64

# API config - 更换为DeepSeek API
API_KEY = "sk-88505d9271714011b8636d2242ba6b59"
BASE_URL = "https://api.deepseek.com"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 配置background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
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
def set_custom_style():  #设置css样式在streamlit中使用这种交互手段来获得更好的zi ding yi
    st.markdown("""
        <style>
        /* 基础组件样式 */
        .main-header { 
            font-size: 42px; #设置字体大小
            font-weight: bold;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 20px;
            animation: fadeInDown 1.6s ease forwards;
        }
        .sub-header {
            font-size: 28px;
            font-weight: bold;
            color: #1E3A8A;
            animation: fadeInLeft 1.6s ease forwards;
            opacity: 0;
        }
        .normal-text {
            font-size: 18px;
            line-height: 1.6;
            animation: fadeIn 1.8s ease forwards;
        }
        .feature-card {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.5s ease, box-shadow 0.5s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 3px 5px 15px rgba(0, 0, 0, 0.2);
        }
        .team-card {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.5s ease, box-shadow 0.5s ease;
        }
        .team-card:hover {
            transform: translateY(-5px);
            box-shadow: 3px 5px 15px rgba(0, 0, 0, 0.2);
        }
        .highlight {
            color: #FF4B4B;
            font-weight: bold;
        }
        .logo-container {
            position: fixed;
            top: 40px;
            right: 20px;
            z-index: 1000;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 50%;
            padding: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 80px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: pulse 2s infinite alternate;
        }
        /* 改进的产品图片容器样式 */
        .product-image-container {
            width: 100%;
            height: 260px;
            overflow: hidden;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            position: relative;
            transition: transform 0.5s ease;
        }
        .product-image-container:hover {
            transform: scale(1.03);
        }
        .product-image-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
        }
        
        /* 动画关键帧定义 */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes fadeInRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            from {
                transform: scale(1);
                box-shadow: 0 0 10px rgba(30, 58, 138, 0.2);
            }
            to {
                transform: scale(1.05);
                box-shadow: 0 0 15px rgba(30, 58, 138, 0.4);
            }
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes zoomIn {
            from {
                transform: scale(0.8);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-20px);
            }
            60% {
                transform: translateY(-10px);
            }
        }
        
        /* 动画类 */
        .animate-fade-in {
            animation: fadeIn 1.6s ease forwards;
            opacity: 0;
        }
        
        .animate-fade-down {
            animation: fadeInDown 1.6s ease forwards;
            opacity: 0;
        }
        
        .animate-fade-up {
            animation: fadeInUp 1.6s ease forwards;
            opacity: 0;
        }
        
        .animate-fade-left {
            animation: fadeInLeft 1.6s ease forwards;
            opacity: 0;
        }
        
        .animate-fade-right {
            animation: fadeInRight 1.6s ease forwards;
            opacity: 0;
        }
        
        .slide-in-right {
            animation: slideInRight 1.6s ease forwards;
            opacity: 0;
        }
        
        .zoom-in {
            animation: zoomIn 1.6s ease forwards;
            opacity: 0;
        }
        
        .bounce {
            animation: bounce 2s ease forwards;
        }
        
        /* 延迟类 */
        .delay-100 { animation-delay: 0.2s; }
        .delay-200 { animation-delay: 0.4s; }
        .delay-300 { animation-delay: 0.6s; }
        .delay-400 { animation-delay: 0.8s; }
        .delay-500 { animation-delay: 1s; }
        .delay-600 { animation-delay: 1.2s; }
        .delay-700 { animation-delay: 1.4s; }
        .delay-800 { animation-delay: 1.6s; }
        
        /* Streamlit组件样式增强 */
        .stButton>button {
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
        }
        button[kind="primary"] {
            animation: pulse 2s infinite alternate;
        }
        .stTextInput>div>div>input {
            transition: all 0.3s ease;
        }
        .stTextInput>div>div>input:focus {
            transform: scale(1.02);
            box-shadow: 0 0 10px rgba(30, 58, 138, 0.3);
        }
        
        /* 底部聊天框新样式 */
        .bottom-chat {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: rgba(255, 255, 255, 0.95);
            box-shadow: 0 -5px 15px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            transition: height 0.6s ease;
            max-height: 400px;
            animation: fadeInUp 1.2s ease;
        }
        
        .chat-message {
            margin-bottom: 15px;
            animation: fadeInUp 0.6s ease;
        }
        
        .chat-message.user {
            display: flex;
            justify-content: flex-end;
        }
        
        .chat-message.bot {
            display: flex;
            justify-content: flex-start;
        }
        
        .chat-bubble {
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 70%;
            word-wrap: break-word;
            transition: transform 0.3s ease;
        }
        
        .chat-bubble:hover {
            transform: translateY(-2px);
        }
        
        .chat-message.user .chat-bubble {
            background-color: #1E3A8A;
            color: white;
        }
        
        .chat-message.bot .chat-bubble {
            background-color: #f1f1f1;
            color: #333;
        }
        
        /* 页面留出底部空间，防止内容被聊天框覆盖 */
        .main-content {
            margin-bottom: 80px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 添加固定位置的logo
    st.markdown(
        f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{get_image_base64('logo.png')}" width="60">
        </div>
        """,
        unsafe_allow_html=True
    )

# 添加一个读取图片并转换为base64的函数
def get_image_base64(image_path):   #这里我要注意要保持图片的大小排版
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Page setup
st.set_page_config(page_title="Smart RMB Dispensing System", layout="wide")

# Add background
try:
    add_bg_from_local('background.jpg')
except Exception as e:
    st.warning(f"Background image failed to load: {str(e)}")

set_custom_style()

# System prompt #替代大模型微调的方法来获得定制化的聊天
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = """永远记住您是一个专业的人民币投放系统助手，由启盛公司开发。为公司服务，
您可以帮助用户解决存钱、取钱和设备维护问题。
本系统采用颜色传感器识别不同面额的人民币，使用距离传感器检测纸币位置，并通过舵机控制投放和取钱机制。
启盛公司是一家专注于智能金融设备开发的高科技企业，这款人民币投放系统是公司的明星产品，用于便捷安全地管理现金。
当用户遇到问题时，请提供专业且友好的建议。"""

# User DB
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "administrator"},
        "user1": {"password": "user123", "role": "administrator"}
    }

# Login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.user_role = None

# 全局聊天历史，用于底部聊天框 v3：修改了固定无意义的东西，
if "bottom_chat_history" not in st.session_state:
    st.session_state.bottom_chat_history = []

# 用户聊天历史，按用户分类 - 统一数据结构为字典列表格式
if "user_chat_histories" not in st.session_state:
    st.session_state.user_chat_histories = {}

# Product promo
def show_product_promotion():
    st.markdown('<div class="main-header">智能人民币投放系统</div>', unsafe_allow_html=True)
    st.markdown('<div class="normal-text">由启盛科技倾力打造的新一代智能现金管理解决方案</div>', unsafe_allow_html=True)
    
    # 使用HTML方式显示产品主图，控制尺寸一致，但是不能直接使用原声的图片，需要使用base64编码，这里是streamlit特殊需要照顾的地方
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin: 30px 0;">
            <div style="width: 70%; max-width: 800px;">
                <div class="product-image-container">
                    <img src="data:image/jpeg;base64,{get_image_base64('overlook.jpg')}" 
                         alt="智能人民币投放系统" class="zoom-in" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <p style="text-align: center; font-style: italic; margin-top: 5px;" class="animate-fade-in delay-200">智能人民币投放系统 - 整体外观</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-header">核心亮点</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card animate-fade-left delay-100">
            <h3>智能识别</h3>
            <p>采用先进的颜色传感器技术，精准识别不同面额人民币，准确率高达99.9%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card animate-fade-left delay-300">
            <h3>安全可靠</h3>
            <p>多重验证机制，防伪技术与物理隔离设计，确保您的资金绝对安全</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card animate-fade-right delay-200">
            <h3>便捷操作</h3>
            <p>人性化界面设计，简单直观的操作流程，老人小孩都能轻松使用</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card animate-fade-right delay-400">
            <h3>智能助手</h3>
            <p>内置AI助手，随时为您解答问题，提供专业指导</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
        <h2 class="animate-fade-up delay-500">未来已来，智能先行</h2>
        <p style="font-size: 18px;" class="animate-fade-up delay-600">立即体验启盛科技带来的智能金融新时代</p>
    </div>
    """, unsafe_allow_html=True)

# Product details
def show_product_details():
    st.markdown('<div class="sub-header">产品详情</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="normal-text animate-fade-in">
        <p>启盛智能人民币投放系统是一款专为银行、商场、社区服务站等场所设计的现金管理设备。系统集成了先进的识别技术和精密的机械控制，能够自动完成存取款、现金分类和保管等功能。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header delay-100">产品外观</div>', unsafe_allow_html=True)
    
    # 使用改进的动画效果展示产品图片（放弃渐入渐出的效果，不适配streamlit的app develop
    product_images_html = f"""
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; margin: 20px 0;">
        <div style="width: 32%;">
            <div class="product-image-container">
                <img src="data:image/jpeg;base64,{get_image_base64('top.jpg')}" alt="顶部视图" class="animate-fade-up" style="animation-delay: 0.3s;">
            </div>
            <p style="text-align: center; margin-top: 5px;" class="animate-fade-up delay-100">顶部视图</p>
        </div>
        <div style="width: 32%;">
            <div class="product-image-container">
                <img src="data:image/jpeg;base64,{get_image_base64('side.jpg')}" alt="侧面视图" class="animate-fade-up" style="animation-delay: 0.6s;">
            </div>
            <p style="text-align: center; margin-top: 5px;" class="animate-fade-up delay-300">侧面视图</p>
        </div>
        <div style="width: 32%;">
            <div class="product-image-container">
                <img src="data:image/jpeg;base64,{get_image_base64('inside.jpg')}" alt="内部结构" class="animate-fade-up" style="animation-delay: 0.9s;">
            </div>
            <p style="text-align: center; margin-top: 5px;" class="animate-fade-up delay-500">内部结构</p>
        </div>
    </div>
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <div style="width: 50%;">
            <div class="product-image-container">
                <img src="data:image/jpeg;base64,{get_image_base64('bottom.jpg')}" alt="底部视图" class="slide-in-right" style="animation-delay: 1.2s;">
            </div>
            <p style="text-align: center; margin-top: 5px;" class="slide-in-right" style="animation-delay: 1.4s;">底部视图</p>
        </div>
    </div>
    """
    
    st.markdown(product_images_html, unsafe_allow_html=True)
    
    # 技术规格部分添加更可靠的动画效果
    st.markdown('<div class="sub-header delay-200">技术规格</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card animate-fade-left" style="animation-delay: 0.4s;">
            <h3>硬件规格</h3>
            <ul>
                <li>尺寸：60cm × 40cm × 100cm</li>
                <li>重量：15kg</li>
                <li>显示屏：上位机平板显示器</li>
                <li>电源：5V 3A</li>
                <li>待机功耗：<1w</li>
                <li>工作功耗：<20w</li>
                <li>上位机：friendlyarm</li>
                <li>下位机：STM32F411</li>
                <li>FPGA：Xilinx</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card animate-fade-right" style="animation-delay: 0.6s;">
            <h3>传感器规格</h3>
            <ul>
                <li>颜色传感器：TCS34725，RGB传感器</li>
                <li>距离传感器：VL6180</li>
                <li>识别精度：>99.9%</li>
                <li>处理速度：<2秒/张</li>
                <li>容纳能力：</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header delay-300">功能详解</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card slide-in-right" style="animation-delay: 0.8s;">
        <h3>自动识别与分类</h3>
        <p>系统采用高精度颜色传感器，能够准确识别不同面额的人民币。先进的图像处理算法能够在0.5秒内完成识别和验证，之后通过精密舵机控制将纸币分类存放。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card slide-in-right" style="animation-delay: 1.0s;">
        <h3>安全存取机制</h3>
        <p>采用双重验证机制确保交易安全。存款时，系统先验证纸币真伪，再确认存入；取款时，通过密码与生物识别双重验证，确保资金安全。所有操作都有详细记录，可追溯查询。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card slide-in-right" style="animation-delay: 1.2s;">
        <h3>智能交互系统</h3>
        <p>内置AI助手，可以语音交互，解答用户问题。系统支持多语言界面，适应不同用户需求。直观的操作流程设计，降低使用门槛，提升用户体验。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header delay-400">应用场景</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card zoom-in" style="text-align: center; animation-delay: 0.4s;">
            <h3>银行网点</h3>
            <p>减轻柜员工作负担，提高服务效率</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card zoom-in" style="text-align: center; animation-delay: 0.6s;">
            <h3>商场超市</h3>
            <p>自助收银区现金处理，降低人力成本</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card zoom-in" style="text-align: center; animation-delay: 0.8s;">
            <h3>社区服务站</h3>
            <p>为居民提供24小时自助现金服务</p>
        </div>
        """, unsafe_allow_html=True)

# Team info
def show_team_info():
    st.markdown('<div class="sub-header">研发团队</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="normal-text animate-fade-in" style="margin-bottom: 30px;">
        <p>启盛科技研发团队由西安电子科技大学的六位优秀学生组成，致力于打造最智能、最安全的金融设备。团队成员各司其职，共同推进项目顺利进行。</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="team-card animate-fade-up" style="animation-delay: 0.3s;">
            <h3>万子墨</h3>
            <p>上位机开发</p>
            <p>西安电子科技大学学生，负责系统上位机设计与开发</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="team-card animate-fade-up" style="animation-delay: 0.6s;">
            <h3>黄永兴</h3>
            <p>FPGA开发工程师</p>
            <p>西安电子科技大学学生，专注FPGA设计与实现</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="team-card animate-fade-up" style="animation-delay: 0.4s;">
            <h3>何家乐</h3>
            <p>微处理器(MCU)工程师</p>
            <p>西安电子科技大学学生，负责底层控制系统开发</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="team-card animate-fade-up" style="animation-delay: 0.7s;">
            <h3>郝家乐</h3>
            <p>网页开发工程师</p>
            <p>西安电子科技大学学生，负责Web前端设计与实现</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="team-card animate-fade-up" style="animation-delay: 0.5s;">
            <h3>黄宪政</h3>
            <p>机械工程师</p>
            <p>西安电子科技大学学生，负责系统机械结构设计与加工</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="team-card animate-fade-up" style="animation-delay: 0.8s;">
            <h3>邬宏扬</h3>
            <p>项目秘书</p>
            <p>西安电子科技大学学生，负责项目协调与文档管理</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header delay-500">团队理念</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card zoom-in" style="animation-delay: 1.0s;">
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

# Operation mode 这里的值可以后期传入服务器和mcu通信如果实现的话  IoT？？
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
    
    # 初始化当前用户的聊天历史
    current_user = st.session_state.current_user
    if current_user not in st.session_state.user_chat_histories:
        st.session_state.user_chat_histories[current_user] = []
    
    current_chat_history = st.session_state.user_chat_histories[current_user]

    # 管理员可编辑系统提示
    if st.session_state.user_role == "administrator":
        with st.expander("编辑背景知识库"):
            st.session_state.system_prompt = st.text_area(
                "系统提示",
                st.session_state.system_prompt,
                height=200
            )
    
    # 清空历史按钮
    if current_chat_history and st.button("清空对话历史"):
        st.session_state.user_chat_histories[current_user] = []
        st.rerun()

    # 用户输入
    user_input = st.text_input("你想说什么？", key="llm_chat_input")

    # 发送按钮
    if st.button("发送", key="llm_chat_send") and user_input:
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
                # 使用DeepSeek API
                from openai import OpenAI
                
                # 创建客户端
                client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
                
                # 发送请求
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    stream=False
                )
                
                # 获取回复
                reply = response.choices[0].message.content
                
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
                reply = "连接失败，请检查网络或API配置。"

            current_chat_history.append((user_input, reply))
            st.session_state.user_chat_histories[current_user] = current_chat_history
            
            st.rerun()

    # 显示对话历史
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

# Main app的底部聊天部分重构
def render_bottom_chat():
    """渲染底部固定聊天界面"""
    
    # 设置底部固定样式
    st.markdown("""
    <style>
    .bottom-chat {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: rgba(255, 255, 255, 0.95);
        box-shadow: 0 -5px 15px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        border-top-left-radius: 15px;
        border-top-right-radius: 15px;
        max-height: 400px;
        overflow: hidden;
        animation: fadeInUp 1.2s ease;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 底部聊天容器
    st.markdown('<div class="bottom-chat">', unsafe_allow_html=True)
    
    # 聊天标题行
    st.markdown("""
    <div style="background-color: #1E3A8A; color: white; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-top-left-radius: 15px; border-top-right-radius: 15px;">
        <h3 style="margin: 0;">智能客服助手</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 展示聊天历史的容器
    chat_container = st.container()
    
    # 添加清除聊天历史按钮
    col_clear, col_spacer = st.columns([1, 5])
    with col_clear:
        if st.button("清空聊天", key="clear_bottom_chat") and st.session_state.bottom_chat_history:
            st.session_state.bottom_chat_history = []
            st.rerun()
    
    # 聊天输入区域
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("发送消息", key="bottom_chat_input", label_visibility="collapsed")
    with col2:
        send_pressed = st.button("发送", key="bottom_send_button")
    
    # 处理历史记录为元组格式 (user_msg, bot_msg)
    display_messages = []
    i = 0
    while i < len(st.session_state.bottom_chat_history):
        if i + 1 < len(st.session_state.bottom_chat_history):
            display_messages.append((st.session_state.bottom_chat_history[i], st.session_state.bottom_chat_history[i+1]))
            i += 2
        else:
            # 处理可能的不成对消息
            display_messages.append((st.session_state.bottom_chat_history[i], "等待回复..."))
            i += 1
    
    # 展示聊天历史
    with chat_container:
        for user_msg, bot_msg in reversed(display_messages):
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                <div style="background-color: #1E3A8A; color: white; padding: 10px 15px; border-radius: 18px; max-width: 70%;">
                    {user_msg}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                <div style="background-color: #f1f1f1; color: #333; padding: 10px 15px; border-radius: 18px; max-width: 70%;">
                    {bot_msg}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 处理用户输入
    if send_pressed and user_input:
        # 添加用户消息到历史
        st.session_state.bottom_chat_history.append(user_input)
        
        # 构建API请求
        messages = [
            {"role": "system", "content": st.session_state.system_prompt}
        ]
        
        # 添加历史消息作为上下文，最多保留10条消息（5组对话）
        history_pairs = []
        i = 0
        while i < len(st.session_state.bottom_chat_history) - 1:  # 不包括刚添加的用户消息
            if i + 1 < len(st.session_state.bottom_chat_history):
                history_pairs.append((st.session_state.bottom_chat_history[i], st.session_state.bottom_chat_history[i+1]))
                i += 2
            else:
                i += 1
        
        # 只保留最近5组对话
        recent_pairs = history_pairs[-5:] if len(history_pairs) > 5 else history_pairs
        
        # 添加到消息列表
        for user_msg, bot_msg in recent_pairs:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": user_input})
        
        with st.spinner("AI正在思考..."):
            try:
                # 使用DeepSeek API
                from openai import OpenAI
                
                # 创建客户端
                client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
                
                # 发送请求
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    stream=False
                )
                
                # 获取回复
                reply = response.choices[0].message.content
                
            except Exception as e:
                reply = f"发生错误: {str(e)}"
            
            # 添加AI回复到历史
            st.session_state.bottom_chat_history.append(reply)
            
            # 刷新页面
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    # 创建带有底部间距的主内容容器
    with st.container():
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
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
                            st.rerun()
                        else:
                            st.error("用户名或密码错误")
                with col2:
                    if st.button("注册"):
                        if username and password:
                            if username not in st.session_state.users_db:
                                st.session_state.users_db[username] = {"password": password, "role": "administrator"}
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
                    st.rerun()
            
            if 'show_password_change' in st.session_state and st.session_state.show_password_change:
                show_password_change()
            
            if 'show_profile' in st.session_state and st.session_state.show_profile:
                show_user_profile()
            
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
        
        st.markdown('</div>', unsafe_allow_html=True)
    

    with st.container():
        render_bottom_chat()


if __name__ == "__main__":
    main()