import yaml

with open('param_data/param_20250902_154451/eav24_trajserver_node.yaml', 'r') as f:
    data = yaml.safe_load(f)

params = data['/eav24/trajserver_node']['ros__parameters']
param_dict = {}

for k, v in params.items():
    if isinstance(v, bool):
        t = 'bool'
    elif isinstance(v, int):
        t = 'int'
    elif isinstance(v, float):
        t = 'float'
    elif isinstance(v, str):
        t = 'string'
    elif isinstance(v, list):
        # 判断列表类型（以第一个元素为准）
        if v and isinstance(v[0], float):
            t = 'list_float'
        elif v and isinstance(v[0], int):
            t = 'list_int'
        elif v and isinstance(v[0], str):
            t = 'list_string'
        else:
            t = 'list'
    else:
        t = 'unknown'
    param_dict[k] = {'type': t, 'value': v}

print(param_dict)