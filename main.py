from config import settings
from service import ElasticSearchService, KafkaConsumer, KafkaProducer


def main():
    es_client = ElasticSearchService(
        host=settings('ES_HOST'),
        port=settings('ES_PORT'),
        index=settings('ES_INDEX'),
        secrets=settings,
    )
    
    producer = KafkaProducer(
        topic=settings('CC_TOPIC_PRODUCER'),
        broker=settings('CC_BROKER'),
        group_id=settings('CC_GROUPID'),
        sr_url=settings('SR_URL'),
        elastic_client=es_client,
        secrets=settings,
    )

    consumer = KafkaConsumer(
        topic=settings('CC_TOPIC_CONSUME'),
        broker=settings('CC_BROKER'),
        group_id=settings('CC_GROUPID'),
        sr_url=settings('SR_URL'),
        elastic_client=es_client,
        producer=producer,
        secrets=settings,
    )

    

    consumer.listener()


if __name__ == '__main__':
    main()
