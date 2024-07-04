import queue
import time
import json
import subprocess
import logging
import _thread

class DownloadTask:
    def __init__(self, args: list, count: int) -> None:
        self.download_args = args
        self.fail_count = count

class HaniTasks:
    def __init__(self) -> None:
        self.paralel_num = 4
        self.fail_threshold = 3
        self.queue = queue.Queue()

    def run(self) -> None:
        for _ in range(self.paralel_num):
            _thread.start_new_thread(self.handle_tasks, ())
        while True:
            time.sleep(1)

    def handle_tasks(self) -> None:
        while True:
            time.sleep(1)

            task = self.queue.get()
            if task is None:
                continue

            logging.info("Start downloading task:%s", task.download_args[0])
            original_args = list(task.download_args)
            download_args = task.download_args
            fail_count = task.fail_count

            try:
                process = subprocess.run(["hani", "dl", *download_args], text=True, capture_output=True, encoding='utf-8')
                outs = process.stderr
                logging.info(outs)
                # Wait for the process to finish and get the return code
                if process.returncode == 0:
                    logging.info("Download success for:%s", download_args[0])
                else:
                    logging.warning("Download failed for:%s", download_args[0])
                    self.reput_task(original_args, fail_count)
            except Exception as err:
                logging.error("Download failed for:%s, %s", download_args[0], str(err))
                self.reput_task(original_args, fail_count)

    def reput_task(self, args: list, fail_count: int) -> None:
        if fail_count > self.fail_threshold:
            logging.error("Fail threshold reached for:%s", args[0])
            return
        self.equeue(DownloadTask(args, fail_count+1))

    def equeue(self, tasks: list) -> None:
        self.queue.put(tasks)

hani_hunter_tasks = HaniTasks()
