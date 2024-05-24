class Resp:
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def is_success(self):
        """判断响应是否成功"""
        return 200 <= self.code < 300

    def get_data(self):
        """获取响应数据"""
        return self.data

    def set_data(self, new_data):
        """设置新的响应数据"""
        self.data = new_data

    def __str__(self):
        """返回响应的字符串表示"""
        return f"Resp(code={self.code}, data={self.data})"

    def __repr__(self):
        """返回响应的正式字符串表示"""
        return self.__str__()

    def to_dict(self):
        """将实例转换为字典"""
        return {
            'code': self.code,
            'data': self.data
        }