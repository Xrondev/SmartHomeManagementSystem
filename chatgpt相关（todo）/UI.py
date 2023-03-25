通过Python实现一个基本的用户操作界面，并为按钮添加事件以从ChatGPT中获取回答：

```python
import tkinter as tk
import openai
openai.api_key = "YOUR_API_KEY"

def send_msg():
    input_text = user_input.get()
    response = openai.Completion.create(
        engine="davinci", prompt=input_text, max_tokens=60
    )
    chat_bot_response = response.choices[0].text
    chatbot_output.delete(1.0, 'end')
    chatbot_output.insert(tk.END, chat_bot_response)

root = tk.Tk()

# 设置窗口标题
root.title("ChatGPT User Interface")

# 创建 Label
user_input_label = tk.Label(root, text="User Input:")
user_input_label.pack()

# 创建用户输入框
user_input = tk.Entry(root)
user_input.pack()

# 创建 Chatbot 输出 Label
chatbot_output_label = tk.Label(root, text="ChatBot Output:")
chatbot_output_label.pack()

# 创建 Chatbot 输出框
chatbot_output = tk.Text(root, height=10)
chatbot_output.pack()

# 创建发送按钮
send_button = tk.Button(root, text="Send", command=send_msg)
send_button.pack()

root.mainloop()
```

导入 Tkinter 库用于创建 GUI 窗口，另外也导入了 OpenAI API 用于与 ChatGPT 进行交互（YOUR_API_KEY 为 API 密钥）。

 `send_msg()` 函数会在用户点击“Send”按钮后被调用。在该函数中，我们获取了用户输入的文本，并调用 OpenAI API 的 `Completion.create()` 方法发送请求到 ChatGPT 并获取响应。我们使用 `insert()` 方法将 ChatBot 的回复输出到输出框中。

创建了窗口和标签，以及用户输入框、Chatbot 输出框和发送按钮。当用户点击“Send”按钮时，`send_msg()` 函数将被调用并显示 ChatGPT 的回答。


