from dataclasses import asdict
from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.error import ProduceError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import (MessageField, SerializationContext,
                                           StringSerializer)



class KafkaProducer:
    def __init__(
        self, topic, broker, group_id, elastic_client, sr_url, secrets
    ):
        self.topic = topic
        self.broker = broker
        self.group_id = group_id
        self.sr_url = sr_url
        self.elastic_client = elastic_client
        self.secrets = secrets

    def delivery_report(self, err, msg):
        """
        Reports the failure or success of a message delivery.
        Args:
            err (KafkaError): The error that occurred on None on success.
            msg (Message): The message that was produced or failed.
        Note:
            In the delivery report callback the Message.key() and Message.value()
            will be the binary format as encoded by any configured Serializers and
            not the same object that was passed to produce().
            If you wish to pass the original object(s) for key and value to delivery
            report callback we recommend a bound callback or lambda where you pass
            the objects along.
        """

        if err is not None:
            print(
                'Delivery failed for User record {}: {}'.format(msg.key(), err)
            )
            return
        print(
            'User record {} successfully produced to {} [{}] at offset {}'.format(
                msg.key(), msg.topic(), msg.partition(), msg.offset()
            )
        )

    def produce(self, message):
        try:
            with open(f'service/resources/schema.avsc') as f:
                schema_str = f.read()

            schema_registry_conf = {'url': self.sr_url}
            schema_registry_client = SchemaRegistryClient(schema_registry_conf)

            avro_serializer = AvroSerializer(
                schema_registry_client, schema_str, asdict(message)
            )

            string_serializer = StringSerializer('utf_8')

            producer_conf = {
                'bootstrap.servers': self.broker,
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': self.secrets.CC_USER,
                'sasl.password': self.secrets.CC_PASSWORD,
            }

            producer = Producer(producer_conf)
            producer.poll(0.0)

            producer.produce(
                topic=self.topic,
                key=string_serializer(str(uuid4())),
                value=avro_serializer(
                    message,
                    SerializationContext(self.topic, MessageField.VALUE),
                ),
                on_delivery=self.delivery_report,
            )

        except KeyboardInterrupt as e:
            print(f'Keyboard: {e}')
        except ValueError:
            print('Invalid input, discarding record...')
        except ProduceError as e:
            print(f'Producer Error: {e}')

        print('\nFlushing records...')
        producer.flush()
