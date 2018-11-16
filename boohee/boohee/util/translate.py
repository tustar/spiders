# -*- coding: utf-8 -*-

import hashlib
import json
import logging
import random
import requests
import zhconv


def update_name(name_cn):
    return name_cn.replace("，又叫...", "") \
        .replace("又叫", "") \
        .replace("...", "") \
        .replace("、", "，")


def chs_to_cht(name_cn):
    return zhconv.convert(name_cn, 'zh-hant')


def chs_to_en(q):
    appKey = '7f9884b758c30ead'
    secretKey = 'vbsEtgcLZzCrtdZR9Zxdnb9diKhbU8Hx'
    url = 'http://openapi.youdao.com/api'
    fromLang = 'zh-CHS'
    toLang = 'EN'
    salt = random.randint(1, 10)  # 中译英

    sign1 = appKey + q + str(salt) + secretKey
    sign = hashlib.md5(sign1.encode(encoding='utf-8')).hexdigest()
    myurl = url + '?q=' + q + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) \
            + '&appKey=' + appKey + '&sign=' + sign
    logging.debug(myurl)

    try:
        response = requests.get(myurl)
        json_data = json.loads(response.text)
        result = json_data['translation'][0]
        return result
    except Exception as e:
        print(e)
    finally:
        pass

    return ''
