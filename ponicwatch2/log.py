"""
Post a log to the rabbitMQ queue
- Used by the Controller, hardware objects or PWO
- Start the process to post payoad in local Sqlite3 db, Cloud db, update Sync Timestamp

Script generates messages
"""
import pika
from json import dumps as json_dumps
from rabbitmqlib import LOGQ, connect



if __name__ == '__main__':
    connection = connect()
    channel = connection.channel()
    logQ = channel.queue_declare(LOGQ)
    message = { }
    for i in range(10):
        message['test'] = i
        channel.basic_publish('',
                              LOGQ,
                              body=json_dumps(message),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
    connection.close()