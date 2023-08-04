import ssl
import pika
import json

class BasicPikaClient:

    def __init__(self, rabbitmq_broker_id, rabbitmq_user, rabbitmq_password, region):

        # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

        url = f"amqps://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_id}.mq.{region}.amazonaws.com:5671"
        parameters = pika.URLParameters(url)
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

class BasicMessageReceiver(BasicPikaClient):

    def get_message(self, queue):
        method_frame, header_frame, body = self.channel.basic_get(queue)
        if method_frame:
            print(method_frame, header_frame, body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return method_frame, header_frame, body
        else:
            print('No message returned')

    def close(self):
        self.channel.close()
        self.connection.close()

    def consume_messages(self, queue):
        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            payload = body.decode('utf-8')
            json_payload = json.loads(payload)
            # do something with the payload
            email = json_payload['email']
            print(email)

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


if __name__ == "__main__":

    # Create Basic Message Receiver which creates a connection
    # and channel for consuming messages.
    basic_message_receiver = BasicMessageReceiver(
         "b-13e19cf1-723e-471b-8d6a-e23d9141cf1f",
        "adaniSurvey",
        "Ad@niSurveyCreds",
        "ap-south-1"
    )

    # # Consume the message that was sent.
    # message = basic_message_receiver.get_message("emailSender")
    # payload = message.decode('utf-8')
    # json_data = json.dumps(payload)
    # email = json_data['email']
    # print(email)

    basic_message_receiver.consume_messages("emailSender")
    


    # Close connections.
    basic_message_receiver.close()