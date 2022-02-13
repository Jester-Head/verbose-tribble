import csv
import time
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from prettytable import PrettyTable
import process as p


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.csv', '*.txt'],
                                                             ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        print("File created - % s." % event.src_path)

    def on_modified(self, event):
        """Creates new list of processes when file updates."""
        print(f'File modified - {event.src_path}')
        process_list = add_process(event)
        display_processes(process_list)

    def on_deleted(self, event):
        print("File deleted - % s." % event.src_path)


def add_process(event=None):
    with open(rf'{event.src_path}', encoding='UTF-16') as csv_file:
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


def filter_score(process, threshold=1):
    """Returns process with VT greater than or equal to threshold"""
    if process.find_vt_score() >= threshold:
        return process


def display_processes(process_list, threshold=1):
    """Organizes processes into table"""
    my_table = PrettyTable(['Signer', 'Company', 'Image Path', 'VT detection', 'VT permalink'])
    for item in process_list:
        filtered_item = filter_score(item, threshold)
        if filtered_item is not None:
            my_table.add_row(
                [filtered_item.signer, filtered_item.company, filtered_item.image_path, filtered_item.vt_detection,
                 filtered_item.vt_permalink])
    print(my_table)


if __name__ == "__main__":
    src_path = r'C:\logger'
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
