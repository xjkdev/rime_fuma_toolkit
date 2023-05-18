from collections import defaultdict
import os
import os.path as osp

input_root = r'C:\Users\Junkun\AppData\Roaming\Rime\remote\rime-ice\cn_dicts'
data_path = osp.join(osp.dirname(osp.abspath(__file__)), 'data')
# 基础码表，用于提供汉字的拼音，也可以是luna_pinyin.dict.yaml
base_dict_file = ['8105.dict.yaml', '41448.dict.yaml']

ziranma_dict1 = {
    "a": "一 丨亅 レ 乛 フ ㄥ",
    "b": "八 丷 卜 冖 宀 匕 比  白 贝  疒  鼻 辟 扁 便 泊 勹",
    "c": "艹 卄 廾  廿 屮 卝 寸 尃 蔡 臧 次 参  曾 从",
    "d": "丶 冫 氵刀刂  リ ㄍ ⺈ 丁 歹 癶 大 亠 盾",
    "e": "二 儿 阝耳 卩  卬",
    "f": "扌  丰  反  方  风  父  缶  巿 番",
    "g": "乚  ㄅ ㄋ 勹 弓 工 广 艮 戈 瓜 谷 革 骨 鬼 夬 罓 𢦏 更 刁",
    "h": "灬  火  禾  户  虍  黑  乊  厷",
    "i": "厂 川 巛 亍 车 虫 臣 辰 赤 齿 髟 豖 朝 镸 长 龹",
    "j": "几  九  己  巾  斤  钅  金  见  臼    角 敫 沮 叚 解夋",
    "k": "コ  凵  匚  冂  口  囗  丂",
    "l": "力  六  立  龙  耒  卤 鹿",
    "m": "木  门  毛  马  米  矛  母 皿  尨 麻  丏 缊",
    "n": "女  牛  牜  ⺧  鸟",
    "o": "日  曰  月  目",
    "p": "ノ  彡  片  皮  疋  ⺪ 攴",
    "q": "七  犭  犬  丌  欠 气  且 酋 亲",
    "r": "亻 人  入  肉",
    "s": "三  罒  巳  纟  糹  糸  厶   丝 石 巸",
    "t": "土 田 夭",
    "u": "水 手  食 飠饣示 礻山 石 尸 十 士 矢 殳 舌 身 豕 鼠 喦",
    "v": "隹  ⺮  爫  爪  豸  止  至  舟",
    "w": "文  亠  攵  夂  夊  ㄨ  王  韦  瓦",
    "x": "彳 小    心  忄    血  彐  夕  习  西  辛 行 乡覀",
    "y": "乙 又 已 讠言 幺 尤 尢 冘 衣 衤羊 牙 业 由 用 页 酉 鱼 雨 羽 聿 乑 乂",
    "z": "辶 廴 子 自 走 足 ⻊卆",
}

bushou_priority = ['扌', '辶', '氵', '冫', '月', '罒', '阝', '王', '攵']


def sort_bushou(x):
    return [bushou_priority.index(i)
            if i in bushou_priority
            else len(bushou_priority) + ord(i)
            for i in x]

def init_ziranma_dict():
    for k in ziranma_dict1:
        ziranma_dict1[k] = ''.join(ch for ch in ziranma_dict1[k] if not ch.isspace())
    ziranma_dict = {}
    for k, v in ziranma_dict1.items():
        for ch in v:
            ziranma_dict[ch] = k
    return ziranma_dict

ziranma_dict = init_ziranma_dict()

chaizi_f = open(osp.join(data_path, "chaizi-jt.1.txt"), encoding='utf8').readlines()
chaizi_dict = {}
for line in chaizi_f:
    splits = line.split('\t')
    chaizi_dict[splits[0]] = list(map(str.rstrip, splits[1:]))

def pinyin2flypy_first(pinyin):
    pymap = {'sh': 'u', 'ch': 'i', 'zh': 'v'}
    if pinyin[:2] in pymap:
        return pymap[pinyin[:2]]
    return pinyin[:1]


def init_shuruma():
    shuruma_dict = {}
    for fname in base_dict_file:
        raw_file_w = open(osp.join(input_root, fname), encoding='utf8').readlines()
        for line in raw_file_w:
            if line.isspace() or line.startswith('#') or '\t' not in line:
                continue

            splits = line.split()
            if len(splits[0]) == 1:
                ma = splits[1].strip()
                shuruma_dict[splits[0]] = pinyin2flypy_first(ma)
    return shuruma_dict

shuruma_dict = init_shuruma()

file = open(osp.join(data_path, "自然码.txt"), encoding='utf8')

fuma_dict = defaultdict(list)
for line in file.readlines():
    splits = line.split('\t')
    if len(splits[0]) > 1:
        continue
    fuma = splits[1].strip()
    if not len(fuma) == 4:
        continue
    fuma = fuma[2:]
    fuma_dict[splits[0]].append(fuma)
file.close()

file = open(osp.join(data_path, "zrm2000.dict.yaml"), encoding='utf8')
for line in file.readlines():
    if '\t' not in line:
        continue
    splits = line.split('\t')
    if len(splits[0]) > 1 and '[' not in splits[0]:
        continue
    if '[' not in splits[0]:
        fuma = splits[1].strip()
    else:
        idx = splits[0].index('[')
        splits[0] = splits[0][:idx]
        fuma = splits[0][idx:].strip('[]')
        if len(splits[0]) != 1:
            continue
    if not len(fuma) == 4:
        continue
    fuma = fuma[2:]
    if fuma not in fuma_dict[splits[0]]:
        fuma_dict[splits[0]].append(fuma)


def get_fuma_l(bushou):
    if bushou in ziranma_dict:
        return ziranma_dict[bushou]
    elif bushou in shuruma_dict:
        return shuruma_dict[bushou][0]
    else:
        return ''


for hanzi_s, items in fuma_dict.items():
    if len(items) == 1:
        continue

    if hanzi_s not in chaizi_dict:
        continue
    chaizi = chaizi_dict[hanzi_s]
    if len(chaizi) > 1:
        min_len = min(map(len, chaizi))
        chaizi = [it for it in chaizi if len(it) == min_len]
        chaizi.sort(key=sort_bushou)
    combine2 = [ch for ch in chaizi[0] if not ch.isspace()]

    new_fuma = []
    if len(combine2) >= 2:
        new_fuma = [get_fuma_l(combine2[0]) + get_fuma_l(combine2[1]),
                    get_fuma_l(combine2[0]) + get_fuma_l(combine2[-1]),
                    get_fuma_l(combine2[1]) + get_fuma_l(combine2[0]),
                    get_fuma_l(combine2[-1]) + get_fuma_l(combine2[0])]

    for fuma in new_fuma:
        if fuma in items:
            fuma_dict[hanzi_s] = [fuma]
            break
    else:
        fuma_dict[hanzi_s] = items[:1]
        print(2, hanzi_s, 'our', new_fuma, 'ziranma', items)

ofile = open(osp.join(data_path, "自然码单字.txt"), 'w', encoding='utf8')
for k, v in fuma_dict.items():
    ofile.write(f"{k}\t{v[0]}\n")
ofile.close()
