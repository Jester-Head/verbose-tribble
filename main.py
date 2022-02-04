import csv
import json

path = 'output.txt'


# filters process by VT rating
def filter_rating(file, value=5):
    vt_threat_list = []
    with open(file, encoding='utf-16') as f:
        reader = csv.DictReader(f)
        reader_list = list(reader)
        for item in reader_list:
            vt_rating = str(item['VT detection']).split("|")

            if vt_rating[0].isdigit():
                if int(vt_rating[0]) >= value:
                    vt_threat_list.append(item)

    return vt_threat_list


results = filter_rating(path)
clean = json.dumps(results, sort_keys=False, indent=4)
print(clean)
