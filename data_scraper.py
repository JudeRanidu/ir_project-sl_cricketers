import requests
from bs4 import BeautifulSoup
import json
from googletrans import Translator
from google.transliteration import transliterate_text


def scrape_player_info(soup, id):
    player_info_keys = ["Full Name", "Born", "Age", "Education", "Batting Style", "Playing Role"]

    player_info_grid = soup.find_all('div', "player_overview-grid")
    player_info_init = player_info_grid[0].find_all('div')

    player_info = {"id": id}

    for detail in player_info_init:
        detail_text = detail.p.getText()
        if (detail_text in player_info_keys):
            if (detail_text == "Born"):
                birth_details = detail.h5.getText().split(',')
                player_info["Birth_Year"] = int(birth_details[1].strip())
                player_info["Birth_District"] = birth_details[2].strip()
            elif (detail_text == "Age"):
                player_info["Age"] = int(detail.h5.getText()[:2])
            elif (detail_text == "Full Name"):
                player_info["Full_Name"] = detail.h5.getText()
            elif (detail_text == "Batting Style"):
                player_info["Batting_Style"] = detail.h5.getText()
            elif (detail_text == "Playing Role"):
                player_info["Playing_Role"] = detail.h5.getText()
            else:
                player_info[detail_text] = detail.h5.getText()

    if not("Education" in player_info.keys()):
        player_info["Education"] = "N/A"
    if not("Batting_Style" in player_info.keys()):
        player_info["Batting_Style"] = "N/A"
    if not("Playing_Role" in player_info.keys()):
        player_info["Playing_Role"] = "N/A"

    return player_info


def scrape_player_stats(soup):
    standings_card_raw = soup.find_all("div", "overflow-hidden")
    tables_raw_check = standings_card_raw[2].find_all("h5")

    for i in range(2):
        if (tables_raw_check[i].getText() == "Batting & Fielding"):
            batting_table_raw = tables_raw_check[i].find_next("table", "table standings-widget-table text-center mb-0 border-bottom")
        else:
            bowling_table_raw = tables_raw_check[i].find_next("table", "table standings-widget-table text-center mb-0 border-bottom")

    player_stats = {}

    # For batting related values
    batting_table_rows_raw = batting_table_raw.find("tbody").find_all("tr")
    for row in batting_table_rows_raw:
        if (row.find("span").getText() == "ODI"):
            batting_table_odi_row = row
            break
        else:
            continue
    batting_values_raw = batting_table_odi_row.find_all("span")

    # For bowling related values
    bowling_table_rows_raw = bowling_table_raw.find("tbody").find_all("tr")
    for row in bowling_table_rows_raw:
        if (row.find("span").getText() == "ODI"):
            bowling_table_odi_row = row
            break
        else:
            continue
    bowling_values_raw = bowling_table_odi_row.find_all("span")

    player_stats["Matches"] = int(batting_values_raw[1].getText())
    player_stats["Runs"] = int(batting_values_raw[4].getText())
    player_stats["Wickets"] = int(bowling_values_raw[5].getText()) if (bowling_values_raw[5].getText() != "-") else 0

    return player_stats


def translate(player):
    player_bio = ""
    player_bio_si = ""
    keys = list(player.keys())
    for key in keys:
        value = player.get(key)
        if (key == "Full_Name"):
            player["Full_Name_si"] = transliterate_text(value, lang_code='si')
        elif (key == "Birth_District"):
            player["Birth_District_si"] = translator.translate(value, dest='si').text
            player_bio_si += "උපන් දිස්ත්‍රික්කය: " + player["Birth_District_si"] + " , "
            player_bio += "Birth District: " + player["Birth_District"] + " , "
        elif (key == "Playing_Role"):
            player["Playing_Role_si"] = sinhala_bat_style_play_role[value] if (value != "N/A") else value
            player_bio_si += "ක්‍රීඩක භූමිකාව: " + player["Playing_Role_si"]
            player_bio += "Playing Role: " + player["Playing_Role"]
        elif (key == "Batting_Style"):
            player["Batting_Style_si"] = sinhala_bat_style_play_role[value] if (value != "N/A") else value
            player_bio_si += "පිතිකරන විලාසය: " + player["Batting_Style_si"] + " , "
            player_bio += "Batting Style: " + player["Batting_Style"] + " , "
        elif (key == "Education"):
            player["Education_si"] = sinhala_schools[value] if (value != "N/A") else value

    print(player_bio_si)
    player["Biography"] = player_bio
    player["Biography_si"] = player_bio_si

    return player


sinhala_schools = {
"Royal College, Colombo": "රාජකීය විද්‍යාලය, කොළඹ",
"Ananda College": "ආනන්ද විද්‍යාලය",
"St. Joseph's College, Maradana": "සාන්ත ජෝසප් විද්‍යාලය, මරදාන",
"St. Joseph's College Maradana": "සාන්ත ජෝසප් විද්‍යාලය, මරදාන",
"Mahanama College, Colombo": "මහනාම විද්‍යාලය, කොළඹ",
"Kalutara Vidyalaya": "කළුතර විද්‍යාලය",
"St. Sebastian's College, Moratuwa": "සාන්ත සෙබස්තියන් විද්‍යාලය, මොරටුව",
"St. Sebastians College, Moratuwa": "සාන්ත සෙබස්තියන් විද්‍යාලය, මොරටුව",
"Prince of Wales College, Moratuwa": "වේල්ස් කුමර විද්‍යාලය, මොරටුව",
"Sri Sumangala College, Panadura":"ශ්‍රී සුමංගල විද්‍යාලය, පානදුර",
"St. Annes College, Kurunegala": "සාන්ත ආනා විද්‍යාලය, කුරුණෑගල",
"S' Thomas' College, Colombo": "සාන්ත තෝමස් විද්‍යාලය, කොළඹ",
"Rahula College": "රාහුල විද්‍යාලය",
"Ananda College, Colombo": "ආනන්ද විද්‍යාලය, කොළඹ",
"St. Peters College - Negombo, Maristella College": "සාන්ත පීතර විද්‍යාලය, මාරිස් ස්ටෙලා විද්‍යාලය, මීගමුව",
"Richmond College, Galle": "රිච්මන්ඩ් විද්‍යාලය, ගාල්ල",
"St. Peter's College": "සාන්ත පීතර විද්‍යාලය",
"St. Peters College, Colombo": "සාන්ත පීතර විද්‍යාලය",
"Maliyadewa College, Kurunegala": "මලියදේව විද්‍යාලය, කුරුණෑගල",
"St. Joseph's College, Colombo": "සාන්ත ජෝසප් විද්‍යාලය, කොළඹ",
"Mahanama Vidyalaya, Panadura": "මහනාම විද්‍යාලය, පානදුර",
"Nalanda College, Colombo": "නාලන්ද විද්‍යාලය, කොළඹ",
"De Mazenod College, Kandana": "ද මස්නෝද් විද්‍යාලය, කඳාන",
"St Anthony's College, Kandy": "සාන්ත අන්තෝනි විද්‍යාලය, මහනුවර",
"Debarawewa Central Hambantota, Mahanama College Colombo, Richmond College, Galle": "දෙබරවැව මධ්‍ය මහා විද්‍යාලය හම්බන්තොට, මහනාම විද්‍යාලය කොළඹ, රිච්මන්ඩ් විද්‍යාලය ගාල්ල",
"Rewatha College, Balapitiya": "රේවත විද්‍යාලය, බලපිටිය",
"Rahula College, Matara":  "රාහුල විද්‍යාලය, මාතර",
"Maris Stella College": "මාරිස් ස්ටෙලා විද්‍යාලය",
"Trinity College, Kandy": "ත්‍රිත්ව විද්‍යාලය, මහනුවර",
"St. Aloysius' College, Galle": "සාන්ත ඇලෝසියස් විද්‍යාලය, ගාල්ල",
"St. Mary's College, Chilaw": "සාන්ත මරියා විද්‍යාලය, හලාවත",
"Vidhyaloka Maha Vidyalaya, Katana": "විද්‍යාලෝක මහා විද්‍යාලය, කටාන",
"Ananda Sastralaya, Kotte": "ආනන්ද ශාස්ත්‍රාලය, කෝට්ටේ",
"St. John's College, Panadura": "සාන්ත ජෝන් විද්‍යාලය, පානදුර",
"Wesley College, Colombo": "වෙස්ලි විද්‍යාලය, කොළඹ",
"St. Servatius College": "සාන්ත සර්වේෂස් විද්‍යාලය",
"Isipathana College, Colombo": "ඉසිපතන විද්‍යාලය, කොළඹ"
}


sinhala_bat_style_play_role = {
"Top order batter":  "ඉදිරි පෙළ පිතිකරු",
"Right hand bat": "දකුණත් පිතිකරු",
"Batter":"පිතිකරු",
"Middle order batter": "මැද පෙළ පිතිකරු",
"Left hand bat": "වමත් පිතිකරු",
"Bowling allrounder": "පන්දු යවන තුන් ඉරියව් ක්‍රීඩක",
"Bowler":"පන්දු යවන්නා",
"Wicketkeeper batter": "කඩුලු රකින පිතිකරු",
"Batting allrounder": "පිතිකරණ තුන් ඉරියව් ක්‍රීඩක",
"Allrounder": "තුන් ඉරියව් ක්‍රීඩක",
"Opening batter": "ආරම්භක පිතිකරු",
}


#main_url = "https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;orderby=runs;size=150;spanmin1=01+Jan+1980;spanval1=span;team=8;template=results;type=batting"
main_url = "https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;orderby=matches;size=150;spanmin1=01+Jan+1990;spanval1=span;team=8;template=results;type=batting"

result = requests.get(main_url)

soup = BeautifulSoup(result.content, 'html.parser')

players_list_init = soup.find_all('tr', "data1")

players_list = []
for i in range(0, 100):
    for j in players_list_init[i].find_all("a", "data-link"):
        players_list.append({"name": j.getText(), "url": j.get("href")})

base_url_player = "https://stats.espncricinfo.com/"

players = []
for i in range(0, 100):
    player_url = base_url_player + players_list[i]["url"]
    response = requests.get(player_url)
    player_soup = BeautifulSoup(response.content, 'html.parser')

    player_data = scrape_player_info(player_soup, i)
    player_data.update(scrape_player_stats(player_soup))

    players.append(player_data)
    print(player_data)
    print('\n')


translator = Translator()
trans_players = []
for player in players:
    trans_player = translate(player)
    trans_players.append(trans_player)


with open('players.json', 'w', encoding='utf-8') as f:
    json.dump(trans_players, f, ensure_ascii=False, indent=4)
