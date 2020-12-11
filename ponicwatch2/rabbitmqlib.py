"""
RabbitMQ pika library wrapper to cover the boilerplates

Script can be executed at repetitive time (like every 5 minutes) to:
- Check the 'logQ' --> consume msg to INSERT in local SQLite db
- Msg are then enqueued in 'syncQ'
- If WIFI detected then consume msg from 'syncQ' to update Cloud service DB
- Success: enqueue in 'updQ' for updating the timestamp in SQLite3
"""
import pika
from json import loads as json_loads

LOGQ, SYNCQ, UPDQ = 'logQ', 'syncQ', 'updQ'
channel = None

def insert_log(channel, method_frame, header_frame, body):
    # print(method_frame.delivery_tag)
    # print(body)
    msg = json_loads(body)
    print("INSERT in DB", msg)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def connect():
    connection = None
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', blocked_connection_timeout=10))
    except (pika.exceptions.ConnectionBlockedTimeout, pika.exceptions.AMQPConnectionError) as err:
        print("Pika exception:", err)
        exit(-1)
    else:
        print("Turn OFF Led1")
    return connection

if __name__ == '__main__':
    # consume the messages from the new added log entries
    connection = connect()
    channel = connection.channel()
    queue_state = channel.queue_declare(LOGQ, durable=True, passive=True, auto_delete=False)
    if queue_state.method.message_count:
        channel.basic_consume(LOGQ, insert_log)
        try:
            channel.start_consuming()
        finally:
            channel.stop_consuming()
    else:
        print("No msg in", LOGQ)
    connection.close()