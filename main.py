import threading
from src.monitor import Monitor
from src.kafka import Producer, Consumer
from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api
from flask_apscheduler import APScheduler
from config.config import Config
import logging
import json

m = Monitor()
app = Flask(__name__)
scheduler = APScheduler()
app.config.from_object('config.config.DevelopmentConfig')
api = Api(app)


def task_producer():
    p = Producer(Config.SERVER_KAFKA, "demo-topic")
    p.create_topic()
    for host, metrics in m.launch_checker().items():
        urls_status = {host: metrics}
        logging.info("Producing to Kafka", urls_status)
        p.produce(json.dumps(urls_status).encode("utf-8"))


def task_consumer():
    c = Consumer(Config.SERVER_KAFKA, "demo-topic")
    c.consume()


class RestApi(Resource):
    def get(self):
        threading.Thread().start()
        return jsonify(m.launch_checker())


api.add_resource(RestApi, '/api')


@app.route("/", methods=["GET"])
def display_returned_statuses():
    return render_template(
        'index.html',
        returned_statuses=m.launch_checker(),
        checkurls=m.open_url_file(),
        )


@app.route('/update', methods=['POST'])
def update():
    return jsonify('', render_template(
        'update.html',
        returned_statuses=m.launch_checker(),
        checkurls=m.open_url_file(),))


if __name__ == '__main__':
    scheduler.add_job(
        id='Task Producer',
        func=task_producer,
        trigger="interval",
        seconds=20
    )
    scheduler.add_job(
        id='Task Consumer',
        func=task_consumer,
        trigger="interval",
        seconds=30
    )
    scheduler.start()
    m.launch_checker()
    app.run()
