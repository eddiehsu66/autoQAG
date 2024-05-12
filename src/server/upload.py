import json
from flask import Flask, request
from flask_sock import Sock
from src.LogModule.AutoPrompt.promptApi import infer_llm_stream
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
sock = Sock(app)

# 确保上传文件夹存在
upload_folder = r'C:\code\src\python\autoQAG\result\upload_file'
os.makedirs(upload_folder, exist_ok=True)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有文件部分在请求中'
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件'
    if file:
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        return f'文件已保存到 {file_path}'


@sock.route('/api/chat')
def chat(ws):
    while True:
        # 接收客户端发送的消息
        message = ws.receive()
        data = json.loads(message)
        if message:
            for response in infer_llm_stream(data['text'],None,None):
                ws.send(response)
        else:
            break
        ws.send('END_OF_MESSAGE')


if __name__ == '__main__':
    app.run(debug=True, port=8888)
