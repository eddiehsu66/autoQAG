import json

from src.LogModule.logParser import log_parser
from src.LogModule.simpleLogExtract import simple_log_extract
from src.server.entity.history import add_message, store_new_history
from src.server.resp import Resp
from flask import Flask, request, make_response
from flask_sock import Sock
from src.config.openaiKit import infer_llm_stream
import os
from src.LogModule.process.processMining import process_mining
from flask_cors import CORS

from src.vector.logRetriever import chat_prompt

app = Flask(__name__)
CORS(app, resources=r'/*')
sock = Sock(app)


@app.route('/api/upload/<uuid:input_uuid>', methods=['POST'])
def upload_file(input_uuid):
    if 'file' not in request.files:
        return '没有文件部分在请求中'
    upload_folder = f"../../cache/logs/{input_uuid}"
    os.makedirs(upload_folder, exist_ok=True)
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件'
    if file:
        file_path = os.path.join(upload_folder, 'Test.log')
        file.save(file_path)
        store_new_history(input_uuid)
        return f'文件已保存'


@sock.route('/api/chat/<uuid>')
def chat(ws, uuid):
    while True:
        # 接收客户端发送的消息
        message = ws.receive()
        data = json.loads(message)
        if uuid != 'demo':
            add_message(uuid, int(data['id']), data['text'], data['isMine'], data['author'])
        response_total = ''
        if message:
            for response in infer_llm_stream(chat_prompt(uuid,data['text']), None, None):
                response_total += response
                ws.send(response)
        else:
            break
        ws.send('END_OF_MESSAGE')
        if uuid != 'demo':
            add_message(uuid, int(data['id']) + 1, response_total, False, 'Assistant')


@app.route('/api/process/<uuid:input_uuid>', methods=['GET'])
def process(input_uuid):
    input_uuid = str(input_uuid)
    log_parser('Test', input_uuid)
    simple_log_extract('Test', input_uuid)
    process_mining(input_uuid)
    if os.path.exists(f'../../cache/logs/{input_uuid}/Test_visual.bpmn'):
        try:
            with open(f'../../cache/logs/{input_uuid}/Test_visual.bpmn', "r", encoding='utf-8') as file:
                file_content = file.read()
            data = Resp(200, file_content)
            response = make_response(data.to_dict())
            response.headers["Content-Type"] = "text/plain; charset=UTF-8"
            return response
        except Exception as e:
            return Resp(500, str(e)).to_dict()


48@app.route('/api/history', methods=['GET'])
def getHistory():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=8888)
