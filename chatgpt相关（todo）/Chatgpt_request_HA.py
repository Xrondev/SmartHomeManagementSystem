import requests
import getpass

# 获取HomeAssistant的IP地址和端口号
ip_address = input("请输入HomeAssistant的IP地址：")
port = input("请输入HomeAssistant的端口号：")

# 获取用户名和密码
username = input("请输入HomeAssistant的用户名：")
password = getpass.getpass("请输入HomeAssistant的密码：")

# 创建一个会话
session = requests.Session()

# 使用提供的用户名和密码进行身份验证
login_url = f"http://{ip_address}:{port}/auth/login"
data = {"username": username, "password": password}
session.post(login_url, json=data)

# 提供一个搜索词，执行搜索
search_term = input("请输入搜索词：")
search_url = f"http://{ip_address}:{port}/api/search"
params = {"query": search_term}
response = session.get(search_url, params=params)

# 输出搜索结果
print(response.json())



import requests
import speech_recognition as sr

# 创建一个Recognizer对象
r = sr.Recognizer()

# 获取语音输入
with sr.Microphone() as source:
    print("请开始说话...")
    audio = r.listen(source)

try:
    # 使用Google语音识别引擎识别语音
    text = r.recognize_google(audio, language="zh-CN")
    print("识别结果: " + text)

    # 向ChatGPT API发送请求
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', 
                             headers={'Authorization': 'Bearer <YOUR_API_KEY>'}, 
                             json={'prompt': text, 'max_tokens': 50})

    # 解析ChatGPT API的响应
    if response.status_code == 200:
        chat_response = response.json()['choices'][0]['text']
        print("ChatGPT回答: " + chat_response)

        # 将ChatGPT回答作为搜索词
        search_term = chat_response

        # 获取HomeAssistant的IP地址和端口号
        ip_address = input("请输入HomeAssistant的IP地址：")
        port = input("请输入HomeAssistant的端口号：")

        # 获取用户名和密码
        username = input("请输入HomeAssistant的用户名：")
        password = getpass.getpass("请输入HomeAssistant的密码：")

        # 创建一个会话
        session = requests.Session()

        # 使用提供的用户名和密码进行身份验证
        login_url = f"http://{ip_address}:{port}/auth/login"
        data = {"username": username, "password": password}
        session.post(login_url, json=data)

        # 执行搜索操作
        search_url = f"http://{ip_address}:{port}/api/search"
        params = {"query": search_term}
        response = session.get(search_url, params=params)
        # 输出搜索结果
        print(response.json())

except sr.UnknownValueError:
    print("语音识别引擎无法识别输入")
except sr.RequestError as e:
    print("无法连接语音识别引擎; {0}".format(e))