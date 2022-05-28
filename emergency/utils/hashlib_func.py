import hashlib


# hash加密
def md(values):
    """
    用于密码加密
    :param values: 需要加密的数据
    :return: 加密后文本
    """
    secret_key = 'username'.encode('utf-8')
    md5_value = hashlib.md5(secret_key)
    md5_value.update(values.encode('utf-8'))
    return md5_value.hexdigest()