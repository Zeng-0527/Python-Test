import re


def reg_search(text, regex_list):
    """
    参数说明：
        text：要匹配的文本
        regex_list：一个字典，key是标签名，value是对应的正则表达式字符串
    """
    result_dict = {}

    # 遍历regex_list里面每一对 key-value
    for key in regex_list:
        pattern = regex_list[key]

        match_list = re.findall(pattern, text)

        if len(match_list) > 0:
            result_dict[key] = match_list
        else:
            result_dict[key] = []

    return result_dict


# ====== 测试代码 ======
if __name__ == "__main__":
    text = """标的证券:本期发行的证券为可交换为发行人所持中国长江电力股份有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。

换股期限:本期可交换公司债券换股期限自可交换公司债券发行结束之日满 12 个月后的第一个交易日起至可交换债券到期日止，即2023 年 6 月 2 日至 2027 年 6 月 1 日。"""

    # 这里是自己写的正则，分别匹配股票代码和日期
    regex_list = {
        '标的证券': r'\d{6}\.\w{2}',
        '换股期限': r'\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日?',
    }

    result = reg_search(text, regex_list)

    print("匹配结果：")
    for key in result:
        print(key + "：" + str(result[key]))
