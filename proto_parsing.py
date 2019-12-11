import custom_python.customized_pb2 as pb2
import google.protobuf.internal as pb
import json, os
from tqdm import tqdm

FNAME = 'synthea/output/fhir/Cristy798_Schroeder447_eaecbe09-10af-41b5-8d0f-a95b941b3ced.json'

def parse_proto(fname):
    message_map = {}
    with open(fname) as fp:
        for line in fp:
            line = line.split()
            if len(line) == 4 and not line[0].endswith('Object'):
                message_map[line[1]] = line[0]
            elif len(line) == 5 and not line[1].endswith('Object'):
                message_map[line[2]] = line[1]
            else:
                continue
    return message_map

def convert_json(js, message_map):
    base = pb2.PatientRecord()
    for item in js['entry']:
        item = item['resource']
        resource = item['resourceType']
        if resource == 'Patient':
            convert_resource(base.patient, item, message_map)
        else:
            new_item = getattr(pb2, resource + 'Object')()
            convert_resource(new_item, item, message_map)
            getattr(base, resource[0].lower() + resource[1:]).append(new_item)
    return base

def convert_resource(base, js, message_map):
    for key in js:
        if type(js[key]) not in (list, dict):
            setattr(base, key, js[key])
            continue
        new_base = getattr(base, key)
        if type(new_base) is pb.containers.RepeatedCompositeFieldContainer:
            for item in js[key]:
                item_base = getattr(pb2, message_map[key])()
                convert_resource(item_base, item, message_map)
                new_base.append(item_base)
        elif type(new_base) is pb.containers.RepeatedScalarFieldContainer:
            new_base.extend(js[key])
        else:
            convert_resource(new_base, js[key], message_map)
        
def write_proto(pr, fname):
    with open(fname, 'wb') as fp:
        fp.write(pr.SerializeToString())

def read_proto(fname):
    with open(fname, 'rb') as fp:
        rec = pb2.PatientRecord()
        rec.ParseFromString(fp.read())
        return rec

def main():
    message_map = parse_proto('customized.proto')
    for fname in tqdm(os.listdir('synthea/output/fhir/')):
        with open('synthea/output/fhir/' + fname, encoding = 'utf-8') as fp:
            js = json.load(fp)
        try:
            pr = convert_json(js, message_map)
            write_proto(pr, 'proto_outputs/' + fname[:-5] + '.pb')
            read_proto('proto_outputs/' + fname[:-5] + '.pb')
        except:
            print(fname)
            raise

if __name__ == '__main__':
    main()