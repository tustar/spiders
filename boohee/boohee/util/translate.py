# -*- coding: utf-8 -*-

import requests
import hashlib
import random
import json

from boohee.util.landconv import Converter


def update_name(name_cn):
    return name_cn.replace("，又叫...", "") \
        .replace("又叫", "") \
        .replace("...", "") \
        .replace("、", "，")


def chs_to_cht(name_cn):
    return Converter('zh-hant').convert(name_cn)


def chs_to_en(name_cn):
    # appKey = 'XXXXX'  # 应用ID，进行注册后可自动获得
    # secretKey = 'XXXXX'  # 应用密钥，进行注册后可自动获得
    appKey = '7f9884b758c30ead'
    secretKey = 'vbsEtgcLZzCrtdZR9Zxdnb9diKhbU8Hx'
    url = 'http://openapi.youdao.com/api'
    fromLang = 'zh-CHS'
    toLang = 'EN'
    salt = random.randint(1, 10)  # 中译英

    sign1 = appKey + name_cn + str(salt) + secretKey
    sign = hashlib.md5(sign1.encode(encoding='utf-8')).hexdigest()
    myurl = url + '?q=' + name_cn + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) \
            + '&appKey=' + appKey + '&sign=' + sign

    r = requests.get(myurl)
    json_data = json.loads(r.text)
    print(json_data)
    name_en = json_data['translation'][0]
    # result = json_data['web'][0]['value'][0]
    return name_en
