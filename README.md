# Search Engine for Sri Lankan Cricketers

**Index No:**   170504N

---

## File Structure
                  
- players.json : Final list of cricketers
- templates : UI related files  
- app.py : Backend of the web app created using Flask 
- indexer.py : Source code to upload data to elasticsearch and create the index
- data_scraper.py :  Source code for scraping data  
- search.py : Search functions used for diferent types of search queries
- requirements.txt : List of required python packages

---

## Setting up the Application

First install elasticsearch and start elasticsearch cluster on port 9200 (default port)

Then execute the following commands (in Windows OS) to create the index in elasticsearch using 
the already available players.json and then start the web app to use for searching

- git clone https://github.com/JudeRanidu/ir_project-sl_cricketers.git
- cd ir_project-sl_cricketers
- python -m venv {venv_name}
- {venv_name}\Scripts\activate.bat
- pip install -r requirements.txt
- python indexer.py
- python app.py

---

## Data Fields

- Name - Sinhala
- Name - English
- Birth Year
- Birth District - Sinhala
- Birth District - English
- Age
- Batting Style - Sinhala
- Batting Style - English
- Playing_Role - Sinhala
- Playing_Role - English
- Matches
- Runs
- Wickets
- Education - Sinhala
- Education - English
- Biography - Sinhala
- Biography - English

---

## Supported Search Queries

- Search by name (Both Sinhala & English)
  - E.g. චමින්ද වාස්, Sanath Jayasuriya
- Search by school (Both Sinhala & English)
  - E.g. ආනන්ද විද්‍යාලය, Richmond College
- Search player biography which includes birth district, batting style & playing role (Both Sinhala & English)
  - E.g. කොළඹ, Galle, වමත් පිතිකරු, Right hand bat, තුන් ඉරියව් ක්‍රීඩක, Bowler
- වැඩිම තරඟ ක්‍රීඩා කළ ක්‍රීඩකයන් [number] or top [number] players played most matches
  - E.g. වැඩිම තරඟ ක්‍රීඩා කළ ක්‍රීඩකයන් 5, top 5 players played most matches
- වැඩිම ලකුණු ලබාගත් ක්‍රීඩකයන් [number] or top [number] run scorers
  - E.g. වැඩිම ලකුණු ලබාගත් ක්‍රීඩකයන් 10, top 10 run scorers
- වැඩිම කඩුලු ලබාගත් ක්‍රීඩකයන් [number] or top [number] wicket takers
  - E.g. වැඩිම කඩුලු ලබාගත් ක්‍රීඩකයන් 15, top 15 wicket takers

---

## Features

- Bilingual support for searching (Both Sinhala & English)
- Intenet classification using cosine similarity
- Range query support
- Search Results are preprocessed before displaying

---

## Scraping, Indexing & Querying

- Data Source for Scraping: ESPNCricnfo - https://stats.espncricinfo.com/ci/engine/stats/index.html
- Data about the top 100 Sri Lankan ODI cricketers that have played the most matches were scraped
- BeautifulSoup used for scraping
- googletrans and google-transliteration-api was respectively used for translation and transliteration
- For indexing the data, standard indexing methods provided in Elasticsearch were used
- For intent classification word tokenization, text vectorization and cosine similarity was used
