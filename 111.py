import yaml
with open("DGS_3130.yaml") as f:
    read_data = yaml.safe_load(f)
    # print(read_data)
for dv in read_data:
    print(dv)
