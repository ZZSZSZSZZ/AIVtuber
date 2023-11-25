import re
from zhconv import convert


def data_cleaning(source: str):
    """弹幕数据清洗"""
    # 剔除制表符(\t)、回车符(\r)、换行符(\n)
    source = source.replace("\t", "").replace("\r", "").replace("\n", "")
    # 将字符串中的英文全部转换为小写
    source = source.lower()
    # 将全角字符转换为半角字符
    source = "".join([Q2B(uchar) for uchar in source])
    # 将繁体字转换为简体字
    source = convert(source, 'zh-cn')
    # 将弹幕中大于等于4个的、连续的、相同的中文汉字合并为3个
    for chinese_character in re.findall(r"([\u4e00-\u9fa5\w])\1{3,}", source):
        source = re.sub("[" + chinese_character[0] + "]{3,}", chinese_character * 3, source)
    # 将弹幕中大于等于4个的、连续的、相同的英文字母合并为3个
    for chinese_character in re.findall(r"([A-Za-z])\1{3,}", source):
        source = re.sub("[" + chinese_character[0] + "]{3,}", chinese_character * 3, source)
    # 将弹幕中大于等于3个的、连续的、相同的标点符号合并为2个
    PUNCTUATION_LIST = [" ", "　", ",", "，", ".", "。", "!", "?"]  # 样例标点符号列表
    punctuation_list = "".join(PUNCTUATION_LIST)
    for match_punctuation in re.findall("([" + punctuation_list + "])\\1{2,}", source):
        source = re.sub("[" + match_punctuation[0] + "]{2,}", match_punctuation * 3, source)
        source = re.sub("-{2,}", "---", source)  # 处理特殊的短横杠
    return source


def Q2B(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:
        return uchar
    return chr(inside_code)


def data_filter():
    filter_str = '你是一个vtuber，以下是弹幕，如果符合回答要求则输出true，否则输出false，回答要求：要判断有没有问答性，禁止回答带有攻击性的问题，禁止回答带有政治的问题，不要回答不会的问题'
