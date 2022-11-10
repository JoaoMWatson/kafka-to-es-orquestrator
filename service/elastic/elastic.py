from dacite import from_dict
from elasticsearch import Elasticsearch, NotFoundError

from service.models import FinancialBusinessOffer


class ElasticSearchService:
    def __init__(self, host, port, index, secrets):
        self.es_client = Elasticsearch(
            [{'host': host, 'port': int(port), 'scheme': 'https'}],
            basic_auth=(secrets.ES_USER, secrets.ES_PASSWORD),
        )
        self.index = index

    def get_document_by_id(self, document_id) -> FinancialBusinessOffer:
        try:
            document = dict(
                self.es_client.get(index=self.index, id=document_id)['_source']
            )
            return from_dict(data=document, data_class=FinancialBusinessOffer)
        except NotFoundError:
            print(f'Elastic document Not found for {document_id}')

    def get_batch(self, batch_size):
        return self.es_client.search(index=self.index, size=batch_size)

    def get_all_documents(self):
        return self.es_client.search(index=self.index, size=10000)
