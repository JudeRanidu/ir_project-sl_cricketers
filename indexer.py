from elasticsearch.helpers import streaming_bulk
from elasticsearch import Elasticsearch, helpers
import json
import tqdm

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def create_index():
    with open('players.json', encoding='utf-8') as file:
        data = json.loads(file.read())

    es.indices.create(
        index='players-index',
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "Full Name": {"type": "text"},
                    "Full Name_si": {"type": "text",
                                     "fields": {
                                        "keyword": {
                                            "type": "keyword"
                                        }
                                     },
                                     },
                    "Birth District": {"type": "text"},
                    "Birth District_si": {"type": "text",
                                          "fields": {
                                            "keyword": {
                                                "type": "keyword"
                                            }
                                          },
                                          },
                    "Education": {"type": "text"},
                    "Education_si": {"type": "text",
                                     "fields": {
                                           "keyword": {
                                               "type": "keyword"
                                           }
                                     },
                                     },
                    "Batting_Style": {"type": "text"},
                    "Batting_Style_si": {"type": "text",
                                         "fields": {
                                            "keyword": {
                                                "type": "keyword"
                                            }
                                         },
                                         },
                    "Playing_Role": {"type": "text"},
                    "Playing_Role_si": {"type": "text",
                                        "fields": {
                                            "keyword": {
                                                "type": "keyword"
                                            }
                                        },
                                        },
                    "Biography": {"type": "text"},
                    "Biography_si": {"type": "text",
                                     "fields": {
                                        "keyword": {
                                            "type": "keyword"
                                        }
                                     },
                                     },
                    'Birth Year': {"type": "integer"},
                    'Age': {"type": "integer"},
                    'Matches': {"type": "integer"},
                    'Runs': {"type": "integer"},
                    'Wickets': {"type": "integer"}
                   }
               },
           },
        ignore=400,
    )

    progress = tqdm.tqdm(unit="docs", total=100)
    successes = 0
    for ok, action in streaming_bulk(client=es, index="players-index", actions=data):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, 100))


if __name__ == "__main__":
    create_index()
