from confluent_kafka import Consumer
from confluent_kafka.error import ConsumeError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext
from dacite import from_dict

from service.models import BusinessOfferingContractCreatedProcessed, business_offering_financial_dataclass
from service.models import BusinessOfferingFinancialContract


class KafkaConsumer:
    def __init__(
        self, topic, broker, group_id, elastic_client, producer, sr_url, secrets
    ):
        self.topic = topic
        self.broker = broker
        self.group_id = group_id
        self.sr_url = sr_url
        self.elastic_client = elastic_client,
        self.producer = producer,
        self.secrets = secrets

    def _create_config(self, type):
        if type == 'consumer':
            config = {
                'bootstrap.servers': self.broker,
                'group.id': self.group_id,
                'auto.offset.reset': 'earliest',
                'enable.auto.commit': 'false',
                'security.protocol': 'SASL_SSL',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': self.secrets.CC_USER,
                'sasl.password': self.secrets.CC_PASSWORD,
            }
        if type == 'schema':
            config = {
                'url': self.sr_url,
                'basic.auth.user.info': '{}:{}'.format(
                    self.secrets.SR_KEY, self.secrets.SR_SECRET
                ),
            }

        return config
        
        
    def create_financial_contract(elastic_document, contract):
        business_offering_financial_contract = BusinessOfferingFinancialContract()

    def message_handler(self, message_raw):
        sr_config = self._create_config('schema')

        schema_registry_client = SchemaRegistryClient(sr_config)
        avro_deserializer = AvroDeserializer(schema_registry_client)

        message_decoded = avro_deserializer(
            message_raw.value(),
            SerializationContext(message_raw.topic(), MessageField.VALUE),
        )

        contract: BusinessOfferingContractCreatedProcessed = from_dict(
            data_class=BusinessOfferingContractCreatedProcessed,
            data=message_decoded,
        )

        return contract

    def elastic_document_search(self, contract):
        return self.elastic_client.get_document_by_id(contract.offer_id())

    def listener(self):
        consumer_config = self._create_config('consumer')

        consumer = Consumer(consumer_config)
        consumer.subscribe([self.topic])

        try:
            while True:
                msg = consumer.poll(timeout=3)
                if msg is None:
                    print('Waiting')
                    continue
                if msg.value():

                    contract = self.message_handler(msg)

                    elastic_document = self.elastic_document_search(contract)
                    
                    financial_contract = self.create_financial_contract(elastic_document, contract)
                    
                    self.producer.produce(message=financial_contract)
                    # consumer.commit()

        except KeyboardInterrupt:
            print('Ending program')

        except ConsumeError as e:
            print(f'Error while consume: {e}')

        finally:
            print('Closing consumer')
            consumer.close()
