Project_Name = "Compiling Text Files 2.0"
from watchdog.observers import Observer  # imports the file-watching engine
from watchdog.events import FileSystemEventHandler  # imports event handler class
import time  # used to keep program running
import os

# custom handler to define what happens when a file changes
class ChangeHandler(FileSystemEventHandler):
    # this function runs whenever any file event occurs
    def on_modified(self, event):
        print(f"Event type: {event.event_type}")  # prints type of event (created/modified/deleted)
        print(f"Path: {event.src_path}")  # prints file path where change happened
        print("-" * 40)  # separator for readability

        if event.event_type == "modified" and not event.src_path.endswith("Combined.txt") and not event.src_path.endswith("Filtered.txt"):
            addfile()

class FilterFile:
    def __init__(self, file, required_count):
        self.file = file
        self.required_count = required_count
    def filter(self):
        unfiltered = self.file.splitlines()
        blank_count = 0
        clean_lines = []
        for line in unfiltered:
            if line == "":
                blank_count += 1
                if blank_count <= self.required_count:
                    clean_lines.append(line)
                else:
                    continue
            else:
                clean_lines.append(line)
                blank_count = 0

        Clean_lines = "\n".join(clean_lines)
        with open("Filtered.txt", "w") as f:
            f.write(Clean_lines)

def addfile():
    files = os.listdir()
    filenames = []
    CombinedContent = Project_Name + ":\n"
    for file in files:
        if file.endswith(".txt") and file != "Combined.txt" and file != "Filtered.txt":
            filenames.append(file)
            with open(file, "r") as f:
                content = f.read()
                CombinedContent += file + " :- " + content + "\n"
    print( filenames, CombinedContent)
    with open("Combined.txt", "w") as f:
        f.write(CombinedContent)
    Filter_file = FilterFile(CombinedContent, 2)
    Filter_file.filter()

def main():
    time.sleep(5)


# main program starts here
if __name__ == "__main__":

    path = "./"  # folder to watch (current directory)

    addfile()

    event_handler = ChangeHandler()  # create handler object

    observer = Observer()  # create observer (watcher)



    # link handler with folder and enable recursive watching
    observer.schedule(event_handler, path, recursive=True)

    observer.start()  # start monitoring files

    print("Watching for changes...")

    try:
        while True:
            time.sleep(3)  # keep program alive

    except KeyboardInterrupt:
        observer.stop()  # stop observer when Ctrl + C is pressed

    observer.join()  # wait until observer fully stops before exiting



