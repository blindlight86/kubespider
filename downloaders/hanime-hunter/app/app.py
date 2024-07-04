import _thread
import logging
import time

from core import webhook
from core import tasks

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s: %(message)s')

def hani_hunter_main():
    _thread.start_new_thread(run_hani_hunter_webhook, ())
    _thread.start_new_thread(run_hani_hunter_tasks, ())
    while True:
        time.sleep(1)

def run_hani_hunter_webhook():
    logging.info("hani_hunter webhook is running...")
    webhook.hani_hunter_server.run(host='0.0.0.0', port=3091)

def run_hani_hunter_tasks():
    logging.info("hani_hunter tasks is running...")
    tasks.hani_hunter_tasks.run()

if __name__ == "__main__":
    hani_hunter_main()
