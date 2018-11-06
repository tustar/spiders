# -*- coding: utf-8 -*-
import re
import urllib

from scrapy.http import Request
from scrapy.spiders import Spider

from boohee.items import CategoryItem, FoodItem
from boohee.util.translate import *


class Spider(Spider):
    name = 'boohee'
    allowed_domains = ['boohee.com']
    SERVER_URL = "http://www.boohee.com"
    SEARCH_URL = "%s/food/search?keyword=" % SERVER_URL
    start_urls = ['{}/food'.format(SERVER_URL)]

    categorys = []
    dishes = ['白菜心拌蜇头', '白灵菇扣鸭掌', '拌豆腐丝', '白切鸡', '拌双耳', '冰梅凉瓜', '冰镇芥兰', '朝鲜辣白菜', '朝鲜泡菜', '陈皮兔肉', '川北凉粉', '刺身凉瓜',
              '豆豉多春鱼', '夫妻肺片', '干拌牛舌', '干拌顺风', '怪味牛腱', '红心鸭卷', '姜汁皮蛋', '酱香猪蹄', '酱肘花', '金豆芥兰', '韭黄螺片', '老北京豆酱', '老醋泡花生',
              '凉拌金针菇', '凉拌西芹云耳', '卤水大肠', '卤水豆腐', '卤水鹅头', '卤水鹅翼', '卤水鹅掌', '卤水鹅胗', '卤水鸡蛋', '卤水金钱肚', '卤水牛腱', '卤水牛舌',
              '卤水拼盘', '卤水鸭肉', '萝卜干毛豆', '麻辣肚丝', '美味牛筋', '蜜汁叉烧', '明炉烧鸭', '泡菜什锦', '泡椒凤爪', '皮蛋豆腐', '乳猪拼盘', '珊瑚笋尖', '爽口西芹',
              '四宝烤麸', '松仁香菇', '蒜茸海带丝', '跳水木耳', '拌海螺', '五彩酱鹅肝', '五香牛肉', '五香熏干', '五香熏鱼', '五香云豆', '腌三文鱼', '盐焗鸡', '盐水虾肉',
              '糟香鹅掌', '酿黄瓜条', '米醋海蜇', '卤猪舌', '三色中卷', '蛋衣河鳗', '盐水鹅肉', '冰心苦瓜', '五味九孔', '明虾荔枝沙拉', '五味牛腱', '拌八爪鱼', '鸡脚冻',
              '香葱酥鱼', '蒜汁鹅胗', '黄花素鸡', '姜汁鲜鱿', '桂花糯米藕', '卤鸭冷切', '松田青豆', '色拉九孔', '凉拌花螺', '素鸭', '酱鸭', '麻辣牛筋', '醉鸡', '可乐芸豆',
              '桂花山药', '豆豉鲫鱼', '水晶鱼冻', '酱板鸭', '烧椒皮蛋', '酸辣瓜条', '五香大排', '三丝木耳', '酸辣蕨根粉', '小黄瓜蘸酱拌苦菜', '蕨根粉拌蛰头老醋黑木耳', '清香苦菊',
              '琥珀核桃', '杭州凤鹅', '香吃茶树菇', '琥珀花生', '葱油鹅肝拌爽口海苔', '巧拌海茸', '蛋黄凉瓜', '龙眼风味肠水晶萝卜', '腊八蒜茼蒿', '香辣手撕茄子', '酥鲫鱼',
              '水晶鸭舌', '卤水鸭舌', '香椿鸭胗', '卤水鸭膀', '香糟鸭卷', '盐水鸭肝', '水晶鹅肝', '豉油乳鸽皇', '酥海带', '脆虾白菜心', '香椿豆腐', '拌香椿苗', '糖醋白菜墩',
              '姜汁蛰皮', '韭菜鲜桃仁', '花生太湖银鱼', '生腌百合南瓜', '酱鸭翅', '萝卜苗', '八宝菠菜', '竹笋青豆', '凉拌苦瓜', '芥末木耳', '炸花生米', '小鱼花生', '德州扒鸡',
              '清蒸火腿鸡片', '熏马哈鱼', '家常皮冻', '大拉皮', '蒜泥白肉', '鱼露白肉', '酱猪肘', '酱牛肉', '红油牛筋', '卤牛腩', '泡椒鸭丝', '拌茄泥', '糖拌西红柿',
              '糖蒜', '腌雪里蕻', '凉拌黄瓜', '两吃干炸丸子', '腐乳猪蹄', '豆豉猪蹄', '木耳过油肉', '海参过油肉', '蒜茸腰片', '红扒肘子', '芫爆里脊丝', '酱爆里脊丝配饼溜丸子',
              '烩蒜香肚丝', '四喜丸子清炸里脊', '软炸里脊', '尖椒里脊丝', '滑溜里脊片', '银芽肉丝', '蒜香烩肥肠', '尖椒炒肥肠', '溜肚块', '香辣肚块', '芫爆肚丝', '软溜肥肠',
              '芽菜回锅肉', '泡萝卜炒肉丝', '米粉排骨', '芽菜扣肉', '东坡肘子', '川式红烧肉', '米粉肉', '夹沙肉', '青豌豆肉丁', '蚂蚁上树', '芹菜肉丝', '青椒肉丝', '扁豆肉丝',
              '冬笋炒肉丝', '炸肉茄合', '脆皮三丝卷烤乳猪', '红烧蹄筋', '清蒸猪脑', '蛋煎猪脑', '菜远炒排骨', '椒盐排骨', '芋头蒸排骨', '蝴蝶骨', '无骨排', '辣白菜炒五花肉',
              '酒醉排骨', '无骨排', '香辣猪扒', '云腿芥菜胆', '板栗红烧肉', '小炒脆骨', '酸豆角肉沫', '五花肉炖萝卜皮', '腊肉红菜苔', '竹筒腊肉', '盐煎肉', '猪肉炖粉条',
              '芸豆焖猪尾', '干豇豆炖猪蹄', '豉汁蒸排骨', '蛋黄狮子头', '酱炒牛柳条', '爆炒牛肋骨', '彩椒牛柳', '白灼肥牛', '菜胆蚝油牛肉', '菜心扒牛肉', '川北牛尾', '川汁牛柳',
              '葱爆肥牛', '番茄炖牛腩', '干煸牛肉丝', '干锅黄牛肉', '罐焖牛肉', '锅仔辣汁煮牛筋丸', '锅仔萝卜牛腩', '杭椒牛柳', '蚝皇滑牛肉', '黑椒牛肋骨', '黑椒牛柳',
              '黑椒牛柳粒', '黑椒牛柳条', '黑椒牛排', '红酒烩牛尾', '胡萝卜炖牛肉', '姜葱爆牛肉', '芥兰扒牛柳', '金蒜煎牛籽粒', '牛腩煲', '清汤牛丸腩', '山药牛肉片', '石烹肥牛',
              '时菜炒牛肉', '水煮牛肉', '酥皮牛柳', '铁板串烧牛肉', '铁板木瓜牛仔骨', '铁板牛肉', '土豆炒牛柳条', '豌豆辣牛肉', '鲜菇炒牛肉', '鲜椒牛柳', '豉汁牛仔骨',
              '香芋黑椒炒牛柳条', '香芋烩牛肉', '小炒腊牛肉', '小笋烧牛肉', '洋葱牛柳丝', '腰果牛肉粒', '中式牛柳', '中式牛排', '孜然烤牛肉', '孜然辣汁焖牛腩', '家乡小炒肉',
              '青豆牛肉粒', '豉油牛肉', '什菜牛肉', '鱼香牛肉', '芥兰牛肉', '雪豆牛肉', '青椒牛肉', '陈皮牛肉', '干烧牛肉', '湖南牛肉', '子姜牛肉', '芝麻牛肉', '辣子牛肉',
              '什锦扒牛肉', '红烧牛蹄筋', '三彩牛肉丝', '西兰花牛柳', '铁锅牛柳', '白灵菇牛柳', '芦笋牛柳', '豆豉牛柳', '红油牛头', '麻辣牛肚', '京葱山珍爆牛柳', '阿香婆石头烤肉',
              '菜远炒牛肉', '凉瓜炒牛肉', '干煸牛柳丝', '柠檬牛肉', '榨菜牛肉', '蒙古牛肉', '椒盐牛仔骨', '辣白菜炒牛肉', '荔枝炒牛肉', '野山椒牛肉丝', '尖椒香芹牛肉丝',
              '堂煎贵族牛肉制作方法黑椒汁香草汁', '香煎纽西兰牛仔骨', '沾水牛肉', '牛肉炖土豆', '清蛋牛肉', '米粉牛肉', '咖喱蒸牛肚', '芫爆散丹', '葱爆羊肉', '大蒜羊仔片', '红焖羊排',
              '葱煸羊腩', '烤羊里脊', '烤羊腿', '卤酥羊腿', '小炒黑山羊', '支竹羊肉煲', '纸包风味羊排', '干羊肉野山菌', '手扒羊排', '烤羔羊', '蒙古手抓肉', '涮羊肉',
              '红烧羊肉', '红焖羊肉', '清炖羊肉', '回锅羊肉', '炒羊肚', '烤全羊', '孜然羊肉', '羊蝎子', '巴蜀小炒鸡', '扒鸡腿', '扒芥香鸡胸', '白椒炒鸡胗', '板栗焖仔鸡',
              '川味红汤鸡', '脆皮鸡', '大千鸡片', '大煮干丝', '当红炸子鸡', '翡翠鲍脯麒麟鸡', '双冬辣鸡球芙蓉鸡片', '干葱豆豉鸡煲', '干锅鸡', '干锅鸡胗', '宫保鸡丁',
              '枸杞浓汁烩凤筋', '花旗参炖竹丝鸡', '鸡茸豆花', '姜葱霸皇鸡', '金针云耳蒸鸡', '咖喱鸡', '可乐凤中翼', '鸿运蒸凤爪', '客家盐焗鸡', '莲藕辣香鸡球', '罗定豆豉鸡',
              '南乳碎炸鸡', '啤酒鸡', '飘香手撕鸡', '麒麟鸡荠菜鸡片', '鲜蘑包公鸡', '沙茶鸡煲', '沙姜焗软鸡', '砂锅滑鸡', '烧鸡肉串', '时菜炒鸡片', '江南百花鸡',
              '四川辣子鸡酥炸鸡胸', '铁板豆豉鸡', '铁板掌中宝', '鲜人参炖土鸡', '香扒春鸡', '杏仁百花脆皮鸡', '杏香橙花鸡脯腰果鸡丁', '一品蒜花鸡', '鱼香鸡片汁烧鸡肉', '美极掌中宝',
              '青瓜鸡丁', '什菜鸡', '芥兰鸡', '雪豆鸡', '甜酸鸡', '陈皮鸡', '干烧鸡', '柠檬鸡', '湖南鸡', '子姜鸡', '豆苗鸡片', '炸八块鸡', '三杯鸡', '葱油鸡',
              '香酥鸡王', '金汤烩鸡脯', '芫爆鹌鹑脯', '枣生栗子鸡西兰花鸡片', '白灵菇鸡片', '芫爆鸡片', '芦笋鸡片', '鸡丁核桃仁', '甜酸鸡腿肉', '怪味鸡丝', '口水鸡',
              '鱼香碎米鸡葱姜油淋鸡', '菜远鸡球', '豉汁黄毛鸡', '子罗炒鸡片', '龙凤琵琶豆腐', '糖醋鸡块', '蜜糖子姜鸡', '苹果咖喱鸡', '糊辣仔鸡', '美极葱香鸡脆骨清蒸童子鸡', '贵妃鸡',
              '江南百花鸡', '烤鸡', '符离集烧鸡', '道口烧鸡', '酱鸡', '熏鸡', '五香鸡', '椒盐鸡', '麻辣鸡', '茶香鸡', '金钱鸡', '芝麻鸡', '叫化鸡', '江米酿鸡',
              '富贵鸡', '纸包鸡', '清蒸全鸡', '半口蘑蒸鸡', '炸鸡肫肝', '一鸡三吃', '牡丹珠圆鸡', '广州文昌鸡', '荸荠鸡片', '时蔬鸡片', '汽锅鸡翅', '清蒸全鸭', '柴把鸭',
              '脆皮鸳鸯鸭全聚德烤鸭', '面鱼儿烧鸭', '双冬鸭', '子姜鸭', '魔芋烧鸭', '五香鸭子', '盐烤荷叶鸭', '鸭粒响铃', '青椒鸭肠', '糟溜鸭三白', '四川樟茶鸭配荷叶饼香熏鸭腰',
              '盐烤荷叶鸭', '口水鸭肠', '芥末鸭掌', '火爆川椒鸭舌', '八珍发菜扒鸭', '赛海蜇拌火鸭丝', '蜜汁烟熏鸭肉卷', '香荽鸭翼', '香酱爆鸭丝', '北菇扒大鸭', '北京烤鸭',
              '彩椒炒火鸭柳', '虫草炖老鸭', '蛋酥樟茶鸭', '冬菜扣大鸭', '参杞炖老鸭', '豆豉芦笋炒鸭柳', '火燎鸭心', '酱爆鸭片', '罗汉扒大鸭', '樱桃汁煎鸭胸', '蜜汁鸭胸',
              '汽锅虫草炖老鸭', '茶树菇炒鹿片', '馋嘴蛙', '笼仔剁椒牛蛙', '泡椒牛蛙', '麻辣玉兔腿', '炸五丝筒全蝎', '酸辣蹄筋', '温拌腰片', '鱼腥草拌米线', '辣味红扒鹿筋',
              '爽口碧绿百叶', '炸炒脆鹿柳', '水煮鹿里脊', '山城血旺', '红烧家兔', '红烧鹿肉', '炸麻雀', '麻辣鹿筋', '豆苗羊肚菌', '川菜白灵菇皇', '干锅茶树菇', '荷塘焖什菌',
              '黄焖山珍菌', '蚝皇原汁白灵菇每位', '鸡油牛肝菌', '三色鲍鱼菇', '砂锅三菌', '烧汁烩南野山菌', '山菌烧豆腐', '双仙采灵芝', '双鲜扒鸡腿菇', '酥炸山菌', '酸辣炒姬菇',
              '泰式煮什菌', '鲜蘑炒蜜豆', '香草蒜茸炒鲜蘑', '香菇扒菜胆', '野菌烧豆腐', '鱼香牛肝菌', '鲍汁花菇', '烩滑籽菇', '干贝鲜腐竹草菇', '清汤干贝鲜蘑', '四宝菌烧素鸡',
              '白灵菇扒鲍片', '鲍鱼海珍煲', '百花鲍鱼卷', '鲍鱼烧牛头', '鲍鱼珍珠鸡', '碧绿香肘扣鲍片', '碧绿原汁鲍鱼', '锅粑鲍鱼', '蚝皇扣干鲍', '蚝皇鲜鲍片', '红烧鲍翅燕',
              '红烧鲍鱼', '红烧南非鲍', '金元鲍红烧肉', '龙井金元鲍', '美国红腰豆扣鲍片', '银芽炒鲍丝', '鲍汁北菇鹅掌', '鲍汁葱烧辽参', '鲍汁豆腐', '鲍汁鹅肝', '鲍汁鹅掌扣辽参',
              '鲍汁花菇烧鹅掌', '鲍汁花胶扣辽参', '鲍汁鸡腿菇', '鲍汁煎鹅肝', '鲍汁扣白灵菇', '鲍汁扣鹅掌', '鲍汁扣花胶皇', '鲍汁扣辽参', '鲍汁扣三宝鲍汁牛肝菌', '白玉蒸扇贝',
              '北极贝刺身', '碧绿干烧澳带', '碧绿鲜带子', '宫保鲜带子', '鸽蛋烧裙边', '果汁银元带子', '姜葱酥炸生蠔', '酱野菌炒胭脂蚌', '金银玉带', '千层酥烤鲜贝',
              '扇贝蒜茸蒸炒豉汁蒸', '碳烧元贝', '铁板酱爆带子', '夏果澳带', '鲜果玉带虾', '珍宝炒带子', '干煎带鱼', '多宝鱼清蒸豉汁蒸过桥芝麻炸多春鱼', '脆炸桂鱼', '干烧桂鱼',
              '桂鱼清蒸油浸松子炸清蒸桂鱼', '松鼠桂鱼', '豆腐烧鱼', '百花酿辽参', '葱爆海参条', '葱烧海参', '高汤京葱扒刺参', '海参鹅掌煲', '蚝汁辽参扣鸭掌红烧牛头扣辽参', '京葱扣辽参',
              '京葱虾籽烧辽参木瓜腰豆煮海参生焗海参煲', '双虾海参煲', '虾仔烧海参', '酱莲藕炒海螺片东古一品螺', '麻辣响螺片', '响螺烧梅花参', '海鲜脆皮豆腐', '海鲜豆腐', '海鲜粉丝煲',
              '海竹笙煮双鲜', '红花汁烩海鲜', '金丝虾球', '金银蒜蒸大花虾', '韭菜炒河虾', '麻婆龙虾仔', '蜜桃水晶丸', '清炒水晶河虾仁', '沙律明虾球', '水晶虾仁', '蒜茸蒸大虾',
              '笋尖炒虾球', '泰式辣椒炒虾仁', '糖醋咕噜虾球', '鲜果沙律虾', '鲜豌豆炒河虾仁', '香葱白果虾', '香菇雪耳烩竹虾', '滋补砂锅大虾', '家乡小炒皇', '香辣虾', '瑶柱烩裙边',
              '羊肚菌爆虾球', '银杏百合炒虾球', '银芽炒虾松', '油焖大虾', '玉簪明虾球', '白灵菇韭黄炒鳕鱼球煎银鳕鱼', '葱烤银鳕鱼', '冬菜银鳕鱼', '蚝黄煎银鳕鱼', '松菇银鳕鱼',
              '泰汁煎银鳕鱼', '特汁银鳕鱼', '香煎银鳕鱼', '酱花枝片', '白灼花枝片', '椒盐吊片', '奇异果炒花枝', '西柠百花鲜鱿', '铁板酱鲜鱿', '香烧鱿鱼', '雪笋花枝片',
              '避风塘焗鱼云', '菜心扒鱼圆', '剁椒鱼头', '沸腾鱼', '锅仔木瓜浸鱼片', '砂锅鱼头', '深海鲽鱼头剁椒葱油', '生焗鱼头', '酸菜鱼', '西湖醋鱼', '虾枣鱼丸豆腐煲',
              '香煎咸鱼', '香烧深海鱼头', '香糟溜鱼片', '腰豆西芹炒鱼松', '野生菌烩乌鱼片', '鲍参翅肚羹', '翅汤浸什菌', '浓汤鸡煲翅供人用川式红烧鱼翅', '高汤鸡丝生翅', '桂花炒鱼翅',
              '红梅蟹粉炒桂花翅', '红烧大鲍翅', '红烧鸡丝翅', '花胶菜胆炖竹笙翅', '火龙燕液翅', '鸡煲海虎翅', '鸡煲牙捡翅', '金肘菜胆炖散翅', '鹿茸养生翅', '木瓜炖翅', '木瓜海虎翅',
              '浓汤鸡火翅', '浓汤鱼肚烩散翅', '浓汁鲍丝翅', '砂锅肚丝翅', '砂锅菇丝翅', '砂锅鸡煲翅', '砂锅裙边翅', '砂锅炒翅', '松茸烩鱼翅', '夏威夷木瓜炖翅', '瑶柱鸡丝烩生翅',
              '红烧排翅', '干贝炖烧翅', '红烧散翅', '海虎翅每两', '金山勾翅每两', '山东海参', '原罐小排翅', '海鲜大煲翅', '浓汁三鲜鱼翅', '浓汁四宝鱼翅', '竹笙笋鸡丝翅',
              '白汁炒鱼唇', '猴头菇扒鱼唇', '浓汁鱼唇', '糟蛋烩鱼唇', '蛋花炒鱼肚', '蚝汁扣鱼肚', '黄扒鱼肚', '菊花乌龙烩鱼肚', '浓汁鱼肚', '青瓜肉松煮鱼肚', '左口鱼豉汁蒸清蒸红烧',
              '佛跳墙', '紫苏煎酿尖椒', '什烩虾', '鱼香虾', '芥兰虾', '雪豆虾', '甜酸虾', '虾龙糊', '干烧虾仁', '湖南虾', '子姜虾', '辣子虾仁', '咖喱虾', '什烩干贝',
              '鱼香干贝', '辣子干贝', '虾子大鸟参', '红烧鸟参', '糖醋全鱼', '豆瓣全鱼', '脆皮全鱼', '清蒸石斑鱼', '清蒸龙利', '干煎龙利', '时菜鱼片', '椒盐鱿鱼', '时菜鱿鱼',
              '豉椒鱿鱼', '宫保鱿鱼', '辣酱蒸鲜鱿', '豆苗大虾', '上海油爆虾', '虾仁跑蛋', '黑椒鱼贝', '糖醋鱿鱼', '炒小卷', '炒大蛤', '九重鲜鲍煎鲳鱼', '马鲛鱼', '蛋黄明虾',
              '如意鳗卷', '葱烧鱼片', '姜丝鱼片', '殷豉鱼片', '咖喱焗鲟', '菠萝虾球', '咸菜虾仁', '豆苗虾仁', '虾仁焖豆腐', '殷豉炒蚵', '葱烧鳗鱼', '三杯中卷', '三杯鳗鱼',
              '酥炸蚵卷', '紫菜虾卷', '玉带干贝酥', '蚝油鲍脯', '凤城煎鱼脯', '川归烧酒虾', '米酱炒蛏肉', '韭黄鳝片', '红鲟米糕', '桂花炒干贝', '豆瓣烧大黄鱼', '炒山瓜仔',
              '豆酥鳕鱼', '椒盐鳕鱼', '椒盐有头虾', '油爆虾', '殷豉炒肉蟹', '桂花炒肉蟹', '咖喱焗肉蟹', '豆酱炒肉蟹', '咸蛋黄炒肉蟹', '殷豉炒珍宝蟹', '桂花炒珍宝蟹',
              '咖喱焗珍宝蟹', '豆酱炒珍宝蟹', '咸蛋黄珍宝蟹', '豉汁蒸白鳝', '清蒸白鳝', '如意炸白鳝', '大蒜烧白鳝', '川汁烧白鳝', '白灼生中虾', '蒜蓉开边蒸生中虾', '药味炖生中虾',
              '盐酥生中虾', '奶油石头焗生中虾', '咖喱串烧生中虾', '鹭香焗生中虾', '清蒸石斑桂鱼左口鱼鲈鱼加吉鱼鳟鱼', '油浸石斑桂鱼左口鱼鲈鱼加吉鱼鳟鱼', '醋烹石斑桂鱼左口鱼鲈鱼加吉鱼鳟鱼',
              '豉汁蒸石斑桂鱼左口鱼鲈鱼加吉鱼鳟鱼', '红烧石斑桂鱼左口鱼鲈鱼加吉鱼鳟鱼', '五柳烧石斑桂鱼左口鱼鲈鱼加吉鱼鳟鱼', '青蒜豆油烧石斑桂鱼左口鱼鲈鱼加吉鱼鳟鱼', '鳟鱼刺身', '豉汁蒸九孔',
              '蒜蓉蒸九孔', '葱油九孔', '香糟焗龙虾', '奶油焗龙虾', '酱爆龙虾', '生蒸龙虾', '三鲜海参', '白扒鱼肚', '山东浓汁鱼翅捞饭', '鲍汁海鲜烩饭', '黄焖鱼翅', '全家福',
              '干焅鱼翅', '白扒鱼翅', '红扒鱼翅', '烧山药海参', '葱烧海参鲍鱼', '葱烧海参牛蹄筋', '烧虾球海参', '醋椒活草鱼', '糟溜活桂鱼', '清炒大龙虾', '椒盐基围虾', '清炒虾仁',
              '干烧虾仁', '豆豉大龙虾', '百合虾球', '干烧虾球', '炸烹虾球', '豆豉虾球', '翡翠虾球', '炸凤尾虾', '扒鱼肚白菜心', '扒鱼肚油菜心', '蚝油小鲍', '扒鲍鱼菜心',
              '扒四宝', '软炸虾仁', '糟烩虾仁', '兰花双味虾仁', '清炒鲍贝', '芙蓉三鲜', '双味软炸鲜贝', '炸烹鲜贝', '清炒贝仁', '赛螃蟹', '芫爆鳝鱼片', '糟溜鳕鱼', '咭汁鱼片',
              '糟溜三白', '爆炒鳝鱼丝', '醋椒活桂鱼葱油活桂鱼', '山东家常焖桂鱼', '葱油泼多宝鱼', '葱油泼牙片鱼', '干烧牙片鱼', '葱油泼石斑鱼', '清蒸闸蟹', '罐焖鸭丝鱼翅',
              '刺参扣鸭掌', '鸭汁鲜凫乌龙', '鸭汤醋椒鱼', '鱼香明虾球', '香辣脆鳝', '老醋蛰头', '王府稣鱼', '家常臊子海参', '宫保带子', '酱鲜椒煎带子', '清汤竹荪海参',
              '桂鱼干烧清蒸酸汤椒盐', '东坡银鳕鱼', '草鱼干烧清蒸水煮酸菜', '宫保大虾肉', '鱼香大虾肉', '顶级头鲍王府极品鲍王府一品鲍', '蟹黄金钩翅', '泡菜鱼翅羹', '肉末辽参',
              '鲍汁扒裙边', '浓汤裙边', '浓汤鱼唇', '浓汤四宝', '青元烩鲜虾', '酸辣蜇头花', '辣炒墨鱼竹百叶', '水煮明虾', '椒香鳝段', '锅巴海三鲜', '板栗烧鳝段', '碧绿椒麻鱼肚',
              '上汤焗龙虾', '蒜蓉蒸龙虾', '椒盐蟹', '咖喱蟹煲', '菜远虾球', '点桃虾球', '油泡虾球', '柠檬虾球', '四川虾球', '豆瓣酱鲜鱿', '韭王象拔蚌', '韭王花枝片',
              '豉汁炒三鲜', '马拉盏炒鱿鱼', '双菇鲜带子', '豉汁炒大蚬', '葱姜生蚝', '豉汁炒青口', '豉汁豆腐蒸带子', '酱炒海茸百合', '百合炒南瓜', '板栗白菜', '白灼时蔬', '炒芥兰',
              '炒生菜', '炒时蔬', '豉汁凉瓜皮', '葱香荷兰豆', '翠豆玉米粒', '冬菇扒菜心', '豆豉鲮鱼油麦菜干贝扒芦笋', '干煸苦瓜', '海茸墨鱼花', '蚝皇扒双蔬', '蚝油扒时蔬',
              '蚝油生菜', '红烧毛芋头', '红枣蒸南瓜', '猴头蘑扒菜心', '虎皮尖椒', '琥珀香芹炒藕粒黄耳浸白玉条', '黄金玉米', '火腿炒蚕豆', '鸡汤竹笙浸时蔬姜汁炒时蔬', '椒盐茄子丁',
              '煎酿鲜茄子', '辣椒炝时蔬', '栗子扒白菜', '萝卜干炒腊肉', '米汤豆苗', '木耳炒山药', '木瓜炖百合', '浓汤金华四宝蔬', '浓汤娃娃菜', '芹香木耳', '清炒蒜茸各式时蔬',
              '清炒蒜茸西兰花', '清炒豆尖', '清煎西红柿', '肉末雪菜', '上汤扒娃娃菜', '上汤鸡毛菜', '上汤芥兰', '上汤浸时蔬', '双耳炒四季', '松仁玉米', '蒜茸炒时蔬', '田园素小炒',
              '铁扒什锦', '西红柿炒蛋', '西芹百合', '乡村大丰收', '雪菜炒豆瓣', '野山红炒木耳', '银杏炒百合', '油盐水浸时蔬', '鱼香茄子', '鱼香茄子煲', '鱼香丝瓜煲玉笋炒酸菜',
              '素什锦', '鱼香芥兰雪豆马蹄', '四季豆', '清炒菠菜', '干贝刈菜', '清炒荷兰豆', '蟹肉丝瓜', '豆腐乳炒通菜', '烫青菜', '小鱼苋菜', '北菇扒菜心', '扁鱼白菜',
              '桂竹笋肉丝', '青叶豆腐', '客家小炒韭菜炒豆干', '九重茄子菜心炒肉片', '扒香菇油菜', '龙须扒菜心', '贝松扒菜心', '口蘑菜胆', '白灼西兰花', '蒜茸芥兰', '鸭黄焗南瓜',
              '枸杞百合西芹', '双冬烧茄子', '芫爆素鳝', '干烧四鲜', '开水白菜', '炝黄瓜', '香油苦瓜', '果汁藕片', '蔬菜沙拉', '麻酱笋条', '四川泡菜', '干煸四季豆清炒芥兰',
              '烧二冬', '油浸娃娃菜', '滑子菇扒菜胆', '蚝油冬菇', '罗汉腐皮卷', '素咕噜肉', '上汤芥菜胆', '蒜蓉豆苗', '干锅笋片', '瓦罐山珍', '酸菜粉丝', '剁椒炒鸡蛋',
              '清炒红菜苔', '剁椒娃娃菜', '剁椒土豆丝', '干煸扁豆', '清炒丝瓜', '水煮萝卜丝', '烤汁茄子', '蚝油茄子', '葱烧黑木耳', '干锅台菇', '沙葱炒鸡蛋', '醋溜豆芽',
              '黄豆芽炒豆腐', '荷塘百花藕', '鲜虾西芹', '杏仁炒南瓜', '地三鲜', '酱烧茄子', '彩虹蒸豆腐', '豉香尖椒炒豆干脆皮豆腐', '锅塌豆腐', '宫保豆腐', '红烧日本豆腐',
              '家常豆腐', '金菇豆腐', '榄菜肉碎炖豆腐', '两虾豆腐', '牛肝菌红烧豆腐', '芹菜炒香干', '日式蒸豆腐', '泰式豆腐', '铁板葱烧豆腐', '西蜀豆花', '乡村小豆腐', '香芹茶干',
              '雪菜炒豆皮', '雪菜虾仁豆腐', '素菜豆腐', '豆豉豆腐', '芝麻豆腐', '左宗豆腐', '五味豆腐', '椒盐豆腐', '辣子豆腐', '咖喱豆腐', '肉酱豆腐', '麻婆豆腐', '三鲜豆腐',
              '虾籽炒豆腐', '面筋百叶', '百叶包肉', '砂锅豆腐', '菠菜豆腐', '鸡血豆腐', '菜豆花', '虾圆玉子豆腐', '冰花炖官燕', '冰糖银耳燕窝', '高汤炖官燕', '红胶官燕',
              '红烧鹿茸血燕', '红烧蟹黄官燕', '红烧血燕', '木瓜炖官燕', '腿汁红烧官燕', '杏汁炖官燕', '冰花炖血燕', '香橙炖官燕', '雪梨官燕', '椰汁冰花炖官燕鱼籽蟹肉烩燕窝',
              '福寿炖燕窝', '一品燕窝', '王府清汤官燕', '冰花芙蓉官燕', '八宝海茸羹', '煲参翅肚羹', '凤凰玉米羹', '桂花雪鱼羮', '鸡茸粟米羮', '九王瑶柱羹', '浓汤鱼肚羮',
              '太极素菜羹', '西湖牛肉豆腐羹', '蟹肉粟米羹', '雪蛤海皇羹', '鱼肚粟米羹', '竹笙海皇羹', '酸辣鱿鱼羹', '台湾肉羹', '干贝芥菜鸡锅', '海鲜盅', '蟹肉烩竹笙', '浓汁三鲜',
              '贝松鱼肚羹', '浓汁木瓜鱼肚', '灵芝金银鸭血羹', '莲子鸭羹', '龙凤羹', '蟹肉豆腐羹', '虫草鸭块汤', '大葱土豆汤', '冬瑶花胶炖石蛙', '豆苗枸杞竹笋汤番茄蛋花汤',
              '凤尾虾丝汤', '极品山珍汤', '家常蛋汤', '老火炖汤每日例汤', '龙虾浓汤', '绿色野菌汤', '萝卜煲排骨汤', '萝卜丝鲫鱼', '美味多菌汤', '浓汤鱼片汤', '山菌时蔬钵',
              '山珍菌皇汤', '上海酸辣汤', '蔬菜海鲜汤', '酸辣海参乌鱼蛋汤', '酸辣汤', '酸辣乌鱼蛋汤', '乌鱼蛋汤', '酸菜肚丝汤', '鲜菌鱼头汤', '香茜鱼片汤', '雪菜大汤黄鱼',
              '亚式浓香鸡汤', '玉米鸡浓汤', '豆腐菜汤', '素菜汤', '本楼汤', '海鲜酸辣汤', '油豆腐粉丝汤', '榨菜肉丝汤', '芋头排骨汤', '枸杞炖蛤', '菠萝凉瓜炖鸡汤', '盐菜肚片汤',
              '咸冬瓜蛤蛎汤', '清汤四宝', '清汤三鲜', '醋椒三片汤', '龙凤汤', '茄汁鸭块汤', '烩鸭舌乌鱼蛋汤', '鸭茸奶油蘑菇汤', '白菜豆腐汤', '竹荪炖菜汤', '黑豆煲鱼头汤',
              '粟米鱼羹', '菜花虾羹', '老酒菌汤', '清汤鸭四宝', '蟹黄鱼翅羹', '玉带芦笋汤', '竹荪银耳汤', '清汤鸭舌羊肚菌', '干贝银丝羹', '蟹黄珍珠羹', '苦瓜蛋清羹',
              '罗宋汤苏伯汤', '鸭架汤', '紫菜蛋花汤', '西红柿鸡蛋汤', '豆腐海带汤', '红汤圆子', '白果煲老鸭', '鲍鱼海珍煲', '鲫鱼黄花煲', '锅仔潮菜银鳕鱼', '锅仔潮式凉瓜猪肚',
              '锅仔鸡汤菌', '锅仔药膳乌鸡', '锅仔鱼肚浸围虾', '海鲜日本豆腐煲', '凉瓜排骨煲', '南乳粗斋煲', '浓汤沙锅三鲜', '南瓜芋头煲', '沙茶鱼头煲', '砂锅白菜粉丝', '砂锅鱼头豆腐',
              '海鲜砂锅', '鱼头砂锅', '腌鲜砂锅', '砂锅小排翅', '砂锅鱼肚', '砂锅海米豆腐', '砂锅萝卜羊排', '砂锅三菇', '砂锅鸡肉丸子', '北菇海参煲', '鸡粒咸鱼茄子煲',
              '粉丝虾米杂菜煲东江豆腐煲', '八珍煲', '柱侯牛腩煲', '虾米粉丝煲', '咸鱼鸡豆腐煲', '核桃肉煲牛肉汤', '梅菜扣肉煲', '米饭', '八宝饭', '鸡汤饭', '翡翠培根炒饭',
              '海皇炒饭', '海南鸡饭', '活虾炒饭', '黑椒香蒜牛柳粒炒饭', '滑蛋虾仁饭', '黑椒猪肉饭', '红肠炒饭', '红烧牛腩饭', '红烧牛肉饭', '黄金大排饭', '火腿炒饭', '鸡蛋炒饭',
              '酱油肉丝炒饭', '京都排骨饭', '腊肉炒饭', '牛肉盖饭', '泡菜炒饭', '蒲烧鳗鱼饭', '茄汁泥肠饭', '青椒牛肉蛋炒饭', '砂锅富豪焖饭', '上海泡饭', '生菜牛肉炒饭',
              '生菜丝咸鱼鸡粒炒饭狮子头饭', '什锦炒饭', '什锦冬瓜粒泡饭', '蔬菜炒饭', '卤肉饭', '泰汁银雪鱼饭', '鲜蘑猪柳配米饭', '招牌羔蟹肉炒饭', '青叶炒饭', '沙茶牛松饭',
              '咸鱼茄粒炒饭', '蒜香排骨饭', '干椒牛肉饭', '香菇牛肉饭', '豉椒鲜鱿饭', '咖喱鱼排饭', '咖喱猪排饭', '杭椒牛柳饭', '美极酱肉虾饭', '三文鱼饭', '可乐鸡饭',
              '香菇排骨饭', '鸡腿饭', '豉汁排骨饭', '台式卤肉饭', '辣子鸡饭', '家常鸡杂饭', '咖喱鸡饭', '咖喱牛肉饭', '老干妈排骨饭', '黑椒牛柳饭', '酱海鲜蛋炒饭', '虾仁炒饭',
              '鸡汤面', '海鲜乌冬汤面', '海鲜虾仁汤面', '什锦汤面', '红烧牛腩汤面', '红烧排骨汤面', '馄饨汤面', '双丸汤面', '虾球清汤面', '虾仁汤面', '雪菜肉丝汤面鸭丝火腿汤面',
              '一品什锦汤面', '榨菜肉丝汤面周公三鲜浓汤面海鲜汤面', '素菜汤面', '炒面', '鸡丝炒面', '梅樱海鲜香炒面', '三鲜焦炒面', '什锦炒面', '鸡丝炒乌冬', '银芽肉丝炒面',
              '酱鸡腿拉面', '拉面', '牛肉拉面', '排骨拉面', '雪菜肉松拉面鲍鱼丝金菇焖伊面', '鲍汁海鲜面', '北京炸酱面', '菜肉馄饨面', '葱油拌面', '担担面', '担仔面', '高汤鸡丝面',
              '高汤榨菜肉丝面', '各式两面黄海虾云吞面', '海鲜噜面', '蚵仔大肠面线', '红烧牛腩面', '黄金大排面', '火腿鸡丝乌冬面', '腊肉西芹卤汁面', '凉面', '蘑菇面', '牛腩面',
              '排骨面', '茄丁肉酱手擀面茄子肉丁打卤面', '肉丝乌冬面', '上海菜煨面', '上海辣酱面', '上汤乌冬面', '狮子头面', '蔬菜面', '四川凉面', '虾排乌冬面', '鲜肉云吞面',
              '香菇鸡丝面', '阳春面', '芝士南瓜面', '猪脚面线', '过桥肥牛汤米线', '干炒牛河', '银芽干炒牛河', '炒河粉', '菜脯叉烧肠粉草菇牛肉肠粉', '豉油蒸肠粉',
              '冬菜牛肉肠粉马蹄鲜虾肠粉清心斋肠粉', '蒸肠粉', '韭黄虾肠粉红烧牛腩米粉', '煎什菜粉果', '清汤牛肉河粉', '酸辣粉', '星州炒米粉', '鸭丝上汤米粉', '肉酱炒米粉',
              '金瓜鲔鱼炒米粉', '菜肉饺子', '猪肉白菜水饺', '猪肉大葱水饺', '猪肉茴香水饺', '鸡蛋韭菜水饺', '猪肉芹菜水饺', '猪肉西葫芦水饺', '香菇油菜水饺', '香茜带子饺', '鲅鱼水饺',
              '瑶柱灌汤饺', '四喜鸭茸饺', '笋尖鲜虾饺', '海天虾饺皇', '蒸饺', '香煎韭菜饺', '高汤水饺', '红油钟水饺', '海鲜汤饺', '酸辣汤水饺', '叉烧包', '叉烧焗餐包',
              '蜜汁叉烧包', '蚝油叉烧包', '煎包', '靖江鸡包仔', '京菜上素包', '生煎包', '豆沙包', '奶黄包', '肉末冬菜包', '三鲜小笼包', '山笋香菇包素菜包', '鲜虾生肉包',
              '香菇鸡肉包香滑芋茸包', '小笼汤包', '蟹籽小笼包', '雪菜包', '萝包', '三鲜水煎包', '酱肉包', '葱油饼', '葱油煎饼', '豆沙锅饼', '海鲜锅饼', '红薯金饼', '韭菜晶饼',
              '萝卜丝酥饼', '肉末烧饼', '肉松松饼', '素馅饼', '鲔鱼松饼', '香酥麻饼', '土豆饼', '芝麻大饼', '芋头饼', '甜烧饼', '咸烧饼', '萝酥饼', '家常饼', '荷叶饼',
              '喜字饼小贴饼子', '川式南瓜饼香脆贴饼子', '黄桥烧饼', '炸南瓜饼', '虾酱小饼', '饼香肉酱鱼籽麻酱糖饼', '炸圈饼', '咸蛋肉饼烙饼', '熘肝尖']

    def __init__(self, total=0):
        self._total = total

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)

        yield from self.crawl_category(response)
        yield from self.crawl_food()

    def crawl_category(self, response):
        values = response.xpath('//div[@id="main"]//li')
        for value in values:
            item = CategoryItem()
            group_url = value.xpath('div[@class="img-box"]//a/@href').extract_first().strip()
            item['group_url'] = "{}{}".format(self.SERVER_URL, group_url)
            item['group_type'] = group_url.split('/')[-1]
            item['thumb_img_url'] = value.xpath(
                'div[@class="img-box"]//a//img/@src').extract_first().strip()
            item['name'] = value.xpath(
                'div[@class="text-box"]//h3//a/text()').extract_first().strip()
            self.categorys.append(item)
            yield item

    def crawl_total(self):
        for _, value in enumerate(self.categorys):
            yield Request(value['group_url'], meta={"category_name": value['name']}, callback=self.parse_total)
        for dish in self.dishes:
            url = str("{}{}".format(self.SEARCH_URL, urllib.request.quote(dish)))
            yield Request(url, meta={"category_name": dish}, callback=self.parse_total)

    def crawl_food(self):
        for index, value in enumerate(self.categorys):
            yield Request(value['group_url'], meta={"category_id": index + 1}, callback=self.parse_food)
        for dish in self.dishes:
            url = str("{}{}".format(self.SEARCH_URL, urllib.request.quote(dish)))
            yield Request(url, meta={"category_id": 11}, callback=self.parse_food)

    def parse_total(self, response):
        self.log('A response from %s just arrived!' % response.url)
        category_name = response.meta["category_name"]
        ins = response.xpath('//span[@class="pagination-sum"]/text()').extract_first()
        ins = ins.replace('\xa0', '')
        category_total = int(re.sub("\D", "", ins))
        logging.debug('%s: %d条', category_name, category_total)
        self.total += category_total
        logging.debug('total: %d条', self.total)

    def parse_food(self, response):
        self.log('A response from %s just arrived!' % response.url)
        category_id = response.meta["category_id"]
        values = response.xpath('//ul[@class="food-list"]//li')
        self.log('items: %d' % len(values))
        for index, value in enumerate(values):
            item = FoodItem()
            try:
                item['category_id'] = category_id
                detail_url = value.xpath(
                    'div[@class="img-box pull-left"]//a/@href').extract_first().strip()
                item['detail_url'] = "{}{}".format(self.SERVER_URL, detail_url)
                item['code'] = detail_url.split('/')[-1]
                item['thumb_img_url'] = value.xpath('div[@class="img-box pull-left"]//a//img/@src').extract_first().strip()
                name = value.xpath('div[@class="text-box pull-left"]//h4//a/text()').extract_first().strip()
                new_name = update_name(name)
                item['name'] = new_name
                calory_weight = value.xpath(
                    'div[@class="text-box pull-left"]//p/text()').extract_first().strip()
                temp = calory_weight.split(' ')
                item['calory'] = re.sub("\D", "", str(temp[0]))
                item['weight'] = re.sub("\D", "", str(temp[-1]))
                item['name_en'] = ''
                item['name_hk'] = chs_to_cht(new_name)
                yield item
            except Exception as e:
                print('Error-Xpath::parse_food[index=%d]%s %s' % (index, response.url, e))
            finally:
                pass

        try:
            next_page = response.xpath('//div[@class="pagination"]//a[@class="next_page"]/@href').extract_first()
            if next_page is None:
                print('Done-Category::parse_food[category_id=%d]' % category_id)
                return
            next_page = "{}{}".format(self.SERVER_URL, next_page)
            yield Request(next_page, meta={"category_id": category_id}, callback=self.parse_food)
        except Exception as e:
            print('Done-Category::parse_food[category_id=%d] %s' % (category_id, e))
        finally:
            pass