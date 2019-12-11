import json

FNAME = 'synthea/output/fhir/Cristy798_Schroeder447_eaecbe09-10af-41b5-8d0f-a95b941b3ced.json'

FIELD_TYPE_CONVERSIONS = {}

def read_json(fname):
    with open(fname, 'r', encoding='utf-8') as fp:
        return json.load(fp)

def write_json(js, fname):
    with open(fname, 'w') as fp:
        json.dump(js, fp)

def unpack_fields(root):
    if type(root) is dict:
        fill = {}
        for key in root:
            fill[key] = unpack_fields(root[key])
        return fill
    if type(root) is list:
        return [unpack_fields(item) for item in root]
    else:
        return str(type(root)) + ' : ex : ' + str(root)

def unpack_objects(root, result = None, name = 'root'):
        if result is None:
            result = {}
        if type(root) is dict:
            if name in result:
                result[name].append(root)
            else:
                result[name] = [root]
            for key, item in root.items():
                if type(item) is dict:
                    unpack_objects(item, result, key)
                    root[key] = key + ' object'
                elif type(item) is list:
                    for element in item:
                        if type(element) is dict:
                            unpack_objects(element, result, key)
                    root[key] = '[' + key + ' object]'
        return result

def main():
    obj = read_json(FNAME)
    st = set()
    for d in obj['entry']:
        st.add(d['resource']['resourceType'])

    schema = {}

    for s in st:
        schema[s] = {}
        for d in obj['entry']:
            if d['resource']['resourceType'] == s:
                schema[s].update(unpack_fields(d['resource']))

    with open('schema.json', 'w') as fp:
        json.dump(schema, fp, indent = 4, sort_keys = True)

    schema2 = unpack_objects(obj)

    with open('schema2.json', 'w') as fp:
        json.dump(schema2, fp, indent = 4, sort_keys = True)

    schema3 = {}
    for item in schema2['resource']:
        if item['resourceType'] not in schema3:
            schema3[item['resourceType']] = item
        else:
            schema3[item['resourceType']].update(item)
    
    with open('schema3.json', 'w') as fp:
        json.dump(schema3, fp, indent = 4, sort_keys = True)

    return schema

if __name__ == '__main__':
    schema = main()
    print(schema)