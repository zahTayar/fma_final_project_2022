from flask import Flask
from pymongo import MongoClient
from src.main.fma.controllers.admin_controller import app_file1
from src.main.fma.controllers.item_controller import app_file2
from src.main.fma.controllers.operation_controller import app_file3
from src.main.fma.controllers.user_controller import app_file4

app = Flask(__name__)
app.register_blueprint(app_file1)
app.register_blueprint(app_file2)
app.register_blueprint(app_file3)
app.register_blueprint(app_file4)
if __name__ == '__main__':
    app.run(port=5500)
