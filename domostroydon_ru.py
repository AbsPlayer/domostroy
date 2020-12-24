import domostroy

def parse_cities():

    domain_cities = domain + "/novostroyki/rostovskaya-oblast/"
    cities = {}
    cities = {"Азов": {"url_city": "azov"},
              "Волгодонск": {"url_city": "volgodonsk"},
              "Новочеркасск": {"url_city": "novocherkassk"},
              "Таганрог": {"url_city": "taganrog"},
              "Городской округ Азов": {"url_city": "gorodskoy-okrug-azov"},
              "Городской округ Батайск": {"url_city": "gorodskoy-okrug-bataysk"},
              "Азовский район": {"url_city": "azovskiy-rayon"},
              "Городской округ Волгодонск": {"url_city": "gorodskoy-okrug-volgodonsk"},
              "Аксайский район": {"url_city": "aksayskiy-rayon"},
              "Мясниковский район": {"url_city": "myasnikovskiy-rayon"},
              "Багаевский район": {"url_city": "bagaevskiy-rayon"},
              "Городской округ Новочеркасск": {"url_city": "gorodskoy-okrug-novocherkassk"},
              "Родионово-Несветайский район": {"url_city": "rodionovo-nesvetayskiy-rayon"},
              "Городской округ Таганрог": {"url_city": "gorodskoy-okrug-taganrog"}
              }
    cities_urls = {}
    cities_urls = {"Ростов": {"url_city": "https://www.domostroydon.ru/novostroyki"}}
    for city, url in cities.items():
        cities_urls[city] = {"url_city": domain_cities + url["url_city"]}
    return cities_urls


domain = "https://www.domostroydon.ru"
cities = parse_cities()
for city, url_city in cities.items():
    zhks = domostroy.parse_zhks(domain, url_city["url_city"])
    for zhk, url_zhk in zhks.items():
        buildings = domostroy.parse_buildings(domain, url_zhk)
        for building, url_building in buildings.items():
            apartments = domostroy.parse_building(url_building)
            buildings[building] = apartments
        zhks[zhk] = buildings
    cities[city] = zhks

for city, city_data in cities.items():
    domostroy.save_to_xlsx(city, city_data)
print("All done!")
