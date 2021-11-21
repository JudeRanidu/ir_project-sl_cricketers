from elasticsearch import Elasticsearch
from nltk.tokenize import word_tokenize

es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])


def keyword_search(query):
    results = es.search(index='players-index', body={
        "size": 10,
        "query": {
            "multi_match": {
                "query": query,
                "type": "best_fields",
                "fields": [
                    "Full_Name", "Full_Name_si", "Education", "Education_si", "Biography", "Biography_si"]
            }
        }
    })
    players = process_results(results)
    print(players)
    return players


def range_search(choice, value):
    if choice == 0 or choice == 1:
        results = es.search(index='players-index', body={
            "size": value,
            "sort": [
                {"Matches": "desc"}
            ]
        })
    elif choice == 2 or choice == 3:
        results = es.search(index='players-index', body={
            "size": value,
            "sort": [
                {"Runs": "desc"}
            ]
        })
    else:
        results = es.search(index='players-index', body={
            "size": value,
            "sort": [
                {"Wickets": "desc"}
            ]
        })

    players = process_results(results)
    print(players)
    return players


def cosine_similarity(query, candidate):
    # tokenization
    query_set = set(word_tokenize(query))
    candidate_set = set(word_tokenize(candidate))

    # form a set containing keywords of both strings
    all_words = query_set.union(candidate_set)

    value = 5  # default value
    query_vec = []
    candidate_vec = []
    for w in all_words:
        if w in query_set:
            query_vec.append(1)
        else:
            query_vec.append(0)

        if w in candidate_set:
            candidate_vec.append(1)
        else:
            candidate_vec.append(0)

        if w.isnumeric():
            value = int(w)

    c = 0
    for i in range(len(all_words)):
        c += query_vec[i] * candidate_vec[i]

    cosine = c / float((sum(query_vec) * sum(candidate_vec)) ** 0.5)
    return cosine, value


def process_results(results):
    players = []
    for i in range(len(results['hits']['hits'])):
        player = results['hits']['hits'][i]['_source']
        player.pop("Full_Name")
        player.pop("Birth_District")
        player.pop("Birth_District_si")
        player.pop("Batting_Style")
        player.pop("Batting_Style_si")
        player.pop("Playing_Role")
        player.pop("Playing_Role_si")
        player.pop("Education")
        player.pop("Biography")
        players.append(player)

    return players


def search(query):
    choices = ["වැඩිම තරඟ ක්‍රීඩා කළ ක්‍රීඩකයන්", "top players played most matches", "වැඩිම ලකුණු ලබාගත් ක්‍රීඩකයන්",
               "top run scorers", "වැඩිම කඩුලු ලබාගත් ක්‍රීඩකයන්", "top wicket takers"]
    cosine_scores = []
    value = 0
    for candidate in choices:
        cosine, value = cosine_similarity(query, candidate)
        cosine_scores.append(cosine)
        value = value

    highest = max(cosine_scores)
    selected_choice = cosine_scores.index(highest)
    if highest > 0.5:
        players = range_search(selected_choice, value)
    else:
        players = keyword_search(query)

    return players

