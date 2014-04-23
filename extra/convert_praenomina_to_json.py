



# {
#     "pk": 1,
#     "model": "promrep.praenomen",
#     "fields": {
#         "abbrev": "A.",
#         "name": "Aulus"
#     }
# },


import json
# Agrippa (Agr.)
fp = open("praenomina.txt")

i = 0
for line in fp.readlines():
    split_line = line.split('(')
    abbrev = split_line[1].strip().strip(')')
    name = split_line[0].strip()

    data = {"pk": i,
                "model": "promrep.praenomen",
                "fields": {
                    "abbrev": abbrev,
                    "name": name
                }
            }

    print json.dumps(data) + ","

    i=i+1


