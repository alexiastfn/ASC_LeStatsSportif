""" App Module """
import os
from app.data_ingestor import DataIngestor
from app.logger import server_logger
from app.task_runner import ThreadPool
from flask import Flask

webserver = Flask(__name__)

if not os.path.exists("results"):
    os.makedirs("results")

webserver.tasks_runner = ThreadPool()


webserver.tasks_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

from app import routes
