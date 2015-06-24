import glob
import os.path
import xml.etree.ElementTree as etree
import codecs

def timestamp(t):
    i = int(t)
    ms = i % 1000
    i /= 1000
    s = i % 60
    i /= 60
    m = i % 60
    i /= 60
    h = i % 60
    return '%02d:%02d:%02d,%03d' % (h, m, s, ms)

def html_to_srt(html_filename):
    srt_filename = os.path.join('srt', os.path.splitext(os.path.basename(html_filename))[0] + '.srt')
    print html_filename, '-->', srt_filename
    fout = codecs.open(srt_filename, mode='w', encoding='utf-8')
    ds_attr = 'data-start'
    idx = 1
    first = True
    tree = etree.parse(html_filename)
    root = tree.getroot()
    for ch in root:
        if ds_attr not in ch.keys(): continue
        cur_ts = timestamp(ch.attrib[ds_attr])
        if first:
            first = False
            pre_ts = cur_ts
            pre_txt = ch.text
            continue
        fout.write(str(idx) + '\n')
        fout.write('%s --> %s' % (pre_ts, cur_ts) + '\n')
        if pre_txt is not None:
            fout.write(pre_txt + '\n')
        fout.write('\n')
        idx += 1
        pre_ts = cur_ts
        pre_txt = ch.text

    # last sentence of this video clip, but the duration is unknown
    # just take a sufficiently large value
    fout.write(str(idx) + '\n')
    fout.write('%s --> %s' % (pre_ts, '23:59:59,999') + '\n')
    if pre_txt is not None:
        fout.write(pre_txt + '\n')
    fout.write('\n')
    fout.close()


if __name__ == '__main__':
    for html_filename in glob.glob('html/*.html'):
        html_to_srt(html_filename)

