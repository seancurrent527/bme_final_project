import json_parsing as jp
import proto_parsing as pp
from tqdm import tqdm
import os

def compare_reading():
    js_list, pr_list = [], []
    for fname in tqdm(os.listdir('json_outputs'), postfix='json reading'):
        js_list.append(jp.read_json('json_outputs/' + fname))
    for fname in tqdm(os.listdir('proto_outputs'), postfix='proto reading'):
        pr_list.append(pp.read_proto('proto_outputs/' + fname))
    return js_list, pr_list

def compare_writing(js_list, pr_list):
    for js in tqdm(js_list, postfix='json writing'):
        jp.write_json(js, 'js_out.json')
    for pr in tqdm(pr_list, postfix='proto writing'):
        pp.write_proto(pr, 'pr_out.pb')

def main():
    js_list, pr_list = compare_reading()
    compare_writing(js_list, pr_list)

if __name__ == '__main__':
    main()