import os
import os.path as osp
import io
import shutil

from ziranma_single import init_shuruma, sort_bushou, init_ziranma_dict, get_fuma_l
from rime_path import get_rime_userdata

input_root = osp.join(get_rime_userdata(), r'remote\rime-ice\cn_dicts')
output_root = osp.join(get_rime_userdata(), r'cn_dicts')
data_path = osp.join(osp.dirname(osp.abspath(__file__)), 'data')

chaizi_f = open(osp.join(data_path, "chaizi-jt.txt"), encoding='utf8').readlines()
chaizi_dict = {}
for line in chaizi_f:
    splits = line.split('\t')
    chaizi_dict[splits[0]] = list(map(str.rstrip, splits[1:]))


# 用于部件发音做辅码
shuruma_dict = init_shuruma()
ziranma_dict = init_ziranma_dict()

# init fuma_dict
fuma_dict = {}
ziranma_danzi = open(osp.join(data_path, "自然码单字.txt"), encoding='utf8').readlines()
for line in ziranma_danzi:
    splits = line.split('\t')
    if len(splits) != 2:
        print(line)
        continue
    fuma_dict[splits[0]] = splits[1].strip()


def already_have_fuma(hanzi, hanzi_s):
    new_fuma = None
    if hanzi_s in fuma_dict:
        new_fuma = fuma_dict[hanzi_s]
    elif hanzi in fuma_dict:
        new_fuma = fuma_dict[hanzi]
    elif hanzi_s in chaizi_dict:
        chaizi = chaizi_dict[hanzi_s]
        if len(chaizi) > 1:
            min_len = min(map(len, chaizi))
            chaizi = [it for it in chaizi if len(it) == min_len]
            chaizi.sort(key=sort_bushou)
        combine2 = [ch for ch in chaizi[0] if not ch.isspace()]
        new_fuma = get_fuma_l(combine2[0]) + get_fuma_l(combine2[1])
        if len(new_fuma) != 2:
            return None
    return new_fuma


def transdict(inf, outf):
    for line in inf:
        if 'luna_pinyin' in line:
            line = line.replace('luna_pinyin', 'flypy_zrmfast')
        if '\t' not in line or line.startswith('#') or line.isspace():
            outf.write(line)
            continue
        splits = line.split('\t')
        if len(splits) == 2:
            hanzi, bianma = splits
            gailv = ''
        else:
            hanzi, bianma, gailv = splits
            gailv = gailv.strip()

        hanzi_s = hanzi
        if len(hanzi) == 1:
            bianma = bianma.strip()
            # 单字转换
            # hanzi_s = converter.convert(hanzi) # simplified
            new_fuma = already_have_fuma(hanzi, hanzi_s)

            if new_fuma is not None:
                new_fuma = bianma + ';' + new_fuma
            else:
                new_fuma = bianma + ';;'
            if gailv != '':
                outf.write(f'{hanzi}\t{new_fuma}\t{gailv}\n')
            else:
                outf.write(f'{hanzi}\t{new_fuma}\n')
        else:
            # 词组转换
            # hanzi_s = converter.convert(hanzi) # simplified
            pinyins = bianma.split()
            if len(hanzi_s) != len(pinyins):
                print(line)
                outf.write(line)
                continue

            new_binama = []
            for h, h_s, b in zip(hanzi, hanzi_s, pinyins):
                b = b.strip()
                new_fuma = already_have_fuma(h, h_s)
                if new_fuma is not None:
                    new_fuma = b + ';' + new_fuma
                else:
                    new_fuma = b + ';;'
                new_binama.append(new_fuma)

            new_code = ' '.join(new_binama)
            if gailv != '':
                outf.write(f'{hanzi}\t{new_code}\t{gailv}\n')
            else:
                outf.write(f'{hanzi}\t{new_code}\n')


if __name__ == '__main__':
    base_dicts = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml']
    for fname in base_dicts:
        infile = open(osp.join(input_root, fname), encoding='utf8').readlines()
        newdataf = io.StringIO()
        transdict(infile, newdataf)
        newdata = newdataf.getvalue()

        with open(osp.join(output_root, fname), 'r', encoding='utf8') as outf:
            olddata = outf.read()
            if newdata == olddata:
                continue
        with open(osp.join(output_root, fname), 'w', encoding='utf8') as outf:
            outf.write(newdata)

    for fname in os.listdir(input_root):
        if fname in base_dicts or not fname.endswith('.yaml'):
            continue

        with open(osp.join(output_root, fname), 'r', encoding='utf8') as oldf, \
                open(osp.join(input_root, fname), 'r', encoding='utf8') as newf:
            olddata = oldf.read()
            newdata = newf.read()
            if olddata == newdata:
                continue
        with open(osp.join(output_root, fname), 'w', encoding='utf8') as outf:
            outf.write(newdata)
