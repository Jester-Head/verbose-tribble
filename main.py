import csv
from ctypes import alignment
from email import header
import fnmatch
import time
from datetime import datetime
from http import server
from tabulate import tabulate
import watchdog
from prettytable import PrettyTable
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import process as p
from serv import MyServer

html_string1 = '<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<title>Process ' \
               'Display</title>\n</head>\n<body>\n '
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
        pattern = r'*done.txt'
        if fnmatch.fnmatch(event.src_path, pattern):
            print(f'{fdate} File modified - {event.src_path}')
            process_list = add_process()
            write_processes_file(process_list)

    def on_deleted(self, event):
        date = datetime.now()
        fdate = date.strftime('%Y-%m-%d %H:%M:%S')
        print(f'{fdate}: File deleted - {event.src_path}')


def add_process():
    file = r'C:\logger\output.txt'
    with open(rf'{file}', encoding='UTF-16') as csv_file:
        process_list = []
        process_list.clear()
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

# Displays in terminal 
def display_processes(process_list, threshold=1):
    """Organizes processes into table"""
    my_table = ['Signer', 'Company', 'Image Path', 'VT detection', 'VT permalink']
    for item in process_list:
        if item.find_vt_score() is not None and item.find_vt_score() >= threshold:
            my_table.append([item.signer, item.company, item.image_path, item.vt_detection, item.vt_permalink])
    print(tabulate(my_table,headers='firstrow', showindex='always', 
         tablefmt='html'))


# Displays results in webserver
def write_processes_file(process_list, threshold=1):
    """Writes results to HTML file"""
    my_table = []
    headers = ['Signer', 'Company', 'Image Path', 'VT detection', 'VT permalink']
    for item in process_list:
        if item.find_vt_score() is not None and item.find_vt_score() >= threshold:
            my_table.append([item.signer, item.company, item.image_path, item.vt_detection, item.vt_permalink])
    with open('results.html', 'w') as f:
        f.write(html_string1 + tabulate(my_table,headers,tablefmt='html',colalign=("left")) + html_string2)
       



if __name__ == "__main__":
    src_path = r'C:\logger'
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    hostName = 'localhost'
    serverPort = 8080 
    MyServer.server_connect(hostName,serverPort)
    try:        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

