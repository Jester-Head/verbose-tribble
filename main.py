import csv
import os
import time
from datetime import datetime
from pathlib import Path

from tabulate import tabulate
from watchdog.events import FileSystemEventHandler
import watchdog.observers

import process as p
from serv import MyServer, RESULTS_FILE

LOG_DIR = Path(r'C:\logger')
OUTPUT_FILE = LOG_DIR / 'output.txt'
DONE_FILE_NAME = 'done.txt'

html_string1 = '''<!DOCTYPE html>
<html lang="en">
<head>
\t<meta charset="UTF-8">
\t<title>Process Display</title>
\t<style>
\t\ttable { font-family: "Century Gothic"; font-size: 13px; border-collapse: collapse; width: 100%; }
\t\tth, td { text-align: left; border-style: double; padding: 3px; }
\t\ttr:nth-child(even) { background-color: #b9ffff; }
\t</style>
</head>
<body>
'''
html_string2 = '\n</body>\n</html>'


class Handler(FileSystemEventHandler):

    def on_created(self, event):
        date = datetime.now()
        fdate = date.strftime('%Y-%m-%d %H:%M:%S')
        print(f'{fdate}: File created - {event.src_path}')

    def on_modified(self, event):
        """Creates new list of processes when file updates."""
        time.sleep(1)
        date = datetime.now()
        fdate = date.strftime('%Y-%m-%d %H:%M:%S')
        src_path = os.fsdecode(event.src_path)
        if Path(src_path).name == DONE_FILE_NAME:
            print(f'{fdate} File modified - {event.src_path}')
            process_list = add_process()
            write_processes_file(process_list)

    def on_deleted(self, event):
        date = datetime.now()
        fdate = date.strftime('%Y-%m-%d %H:%M:%S')
        print(f'{fdate}: File deleted - {event.src_path}')


def add_process():
    """Reads the Autoruns CSV and keeps the entries that have a VirusTotal result."""
    process_list = []
    with open(OUTPUT_FILE, encoding='UTF-16', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            signer = line['Signer']
            company = line['Company']
            image_path = line['Image Path']
            vt_detection = line['VT detection']
            if vt_detection:
                vt_permalink = line['VT permalink']
                new_process = p.Process(
                    signer, company, image_path, vt_permalink, vt_detection)
                process_list.append(new_process)
    return process_list


# Displays results in webserver
def write_processes_file(process_list, threshold=1):
    """Writes results to HTML file"""
    my_table = []
    headers = ['Signer', 'Company', 'Image Path', 'VT detection', 'VT permalink']
    for item in process_list:
        score = item.find_vt_score()
        if score is not None and score >= threshold:
            my_table.append([item.signer, item.company, item.image_path, item.vt_detection, item.vt_permalink])
    # Column alignment comes from the CSS in html_string1
    table = tabulate(my_table, headers, tablefmt='html')
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        f.write(html_string1 + table + html_string2)


if __name__ == "__main__":
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=str(LOG_DIR), recursive=True)
    observer.start()
    hostName = 'localhost'
    serverPort = 8080
    try:
        # Blocks until Ctrl+C, then the file watcher is stopped too
        MyServer.server_connect(hostName, serverPort)
    finally:
        observer.stop()
        observer.join()
