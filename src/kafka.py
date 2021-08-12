from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka import errors
from kafka.admin import NewTopic
from src.postgres import Postgres
from config.config import Config
from datetime import datetime
import json


class Producer:
    """Kafka Producer object"""
    def __init__(self, server, topic):
        self.server = server
        self.topic = topic

        try:
            self.producer = KafkaProducer(
                    bootstrap_servers=self.server,
                    security_protocol="SSL",
                    ssl_cafile=Config.ssl_cafile,
                    ssl_certfile=Config.ssl_certfile,
                    ssl_keyfile=Config.ssl_keyfile
            )
        except errors.NoBrokersAvailable as e:
            print(f'Error connecting to Kafka broker: {e}')

    def create_topic(self):
        """This function create a topic in Kafka"""
        admin = KafkaAdminClient(bootstrap_servers=self.server,
                                 security_protocol="SSL",
                                 ssl_cafile=Config.ssl_cafile,
                                 ssl_certfile=Config.ssl_certfile,
                                 ssl_keyfile=Config.ssl_keyfile
                                 )
        try:
            topic = NewTopic(name=self.topic,
                             num_partitions=1,
                             replication_factor=2)
            admin.create_topics([topic])
        except errors.TopicAlreadyExistsError:
            print("topic exists")

    def produce(self, message: bytes):
        """This function send messages to Kafka topic"""
        self.producer.send(self.topic, message)


class Consumer:
    """Kafka Consumer object"""
    def __init__(self, server, topic):
        self.server = server
        self.topic = topic

        try:
            self.consumer = KafkaConsumer(
                self.topic,
                auto_offset_reset="latest",
                bootstrap_servers=self.server,
                client_id="demo-client-1",
                group_id="demo-group",
                security_protocol="SSL",
                ssl_cafile=Config.ssl_cafile,
                ssl_certfile=Config.ssl_certfile,
                ssl_keyfile=Config.ssl_keyfile,
            )
        except Exception as e:
            print(f'Error connecting to Kafka broker: {e}')
            raise e
        self.consumer.poll(timeout_ms=1)

    def consume(self):
        """This function consume Kafka data and insert data into a Postgres table"""
        raw_msgs = self.consumer.poll(timeout_ms=1000)
        obj = Postgres(Config.DBHOST,
                       Config.DB,
                       Config.DBUSER,
                       Config.DB_PASSWORD,
                       Config.DBTABLE
        )
        for tp, msgs in raw_msgs.items():
            for msg in msgs:
                my_dict = json.loads(msg.value.decode('utf-8'))
                data = list(my_dict.values())[0]
                datetime_object = datetime.strptime(data[3], '%y-%m-%d %a %H:%M:%S')
                print([*my_dict.keys()][0], data[0], data[1], datetime_object)
                obj.db_insert([*my_dict.keys()][0], data[0], data[1], datetime_object)
        return self.consumer.commit()