import os.path as osp

import opencc

from rime_path import get_rime_userdata


converter = opencc.OpenCC('t2s.json')

input_root = get_rime_userdata()
output_root = osp.join(get_rime_userdata(), r'cn_dicts')


def transdict(inf, outf):
    for line in inf:
        if 'luna_pinyin' in line:
            line = line.replace('luna_pinyin', 'luna_simp')
        if line.startswith('#') or line.isspace() or ':' in line:
            outf.write(line)
            continue
        if '\t' not in line:
            line = converter.convert(line)
            outf.write(line)
            continue
        hanzi, rest = line.split('\t', maxsplit=1)
        hanzi = converter.convert(hanzi)
        outf.write(hanzi + '\t' + rest)
    outf.close()


if __name__ == '__main__':
    for fname in ['luna_pinyin.computer.dict.yaml', 'luna_pinyin.poetry.dict.yaml', 'luna_pinyin.math.dict.yaml']:
        infile = open(osp.join(input_root, fname), encoding='utf8').readlines()
        outfname = fname.replace('luna_pinyin', 'luna_simp')
        outf = open(osp.join(output_root, outfname), 'w', encoding='utf8')

        transdict(infile, outf)
