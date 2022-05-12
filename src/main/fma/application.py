from flask import Flask
from src.main.fma.controllers.admin_controller import app_file1
from src.main.fma.controllers.item_controller import app_file2
from src.main.fma.controllers.operation_controller import app_file3
from src.main.fma.controllers.user_controller import app_file4
from src.main.fma.apis.worker import worker
from time import sleep
from datetime import datetime
from multiprocessing import Process
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_file1)
app.register_blueprint(app_file2)
app.register_blueprint(app_file3)
app.register_blueprint(app_file4)


def exec_worker():
    worker_min = 12*60
    w = worker()
    while True:
        sleep(60 * worker_min)
        print("start updating db")
        zah = datetime.now()
        print(zah)
        w.update_db()
        print(datetime.now() - zah)


def run_app():
    app.run(port=5500)


# Helper function to easly parallelize multiple functions
def parallelize_functions(*functions):
    processes = []
    for function in functions:
        p = Process(target=function)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


if __name__ == '__main__':
    parallelize_functions(run_app, exec_worker)
