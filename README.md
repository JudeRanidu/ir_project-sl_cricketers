**Index No:**   170504N

---

## File Structure
                  
- players.json : Final list of cricketers
- templates : UI related files  
- app.py : Backend of the web app created using Flask 
- indexer.py : Source code to upload data to elasticsearch and create the index
- data_scraper.py :  Source code for scraping data  
- search.py : Search functions used for diferent types of search queries
- requirements.txt : List of required python pacakages

---

## Setting up the Application

First install elasticsearch and start elasticsearch cluster on port 9200 (default port)

Then execute the following commands (in Windows OS) to create the index in elasticsearch using the already
available players.json and then start the web app to use for searching

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
