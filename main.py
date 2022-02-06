import csv
from process import Process

path = 'output.txt'


# Move later
def add_process(file):
    process_list = []
    with open(file, encoding='utf-16') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for process in csv_reader:
            signer = process['Signer']
            company = process['Company']
            image_path = process['Image Path']
            vt_detection = process['VT detection']
            if vt_detection:
                vt_permalink = process['VT permalink']
                new_process = Process(signer, company, image_path, vt_permalink, vt_detection)
                process_list.append(new_process)
    return process_list


# Move later
def filter_score(process, threshold=1):
    return process.find_vt_score() >= threshold
