import domostroy

def parse_cities():

    domain = "https://domostroyrf.ru"
    domain_cities = domain + "/novostroyki/voronezhskaya-oblast/"
    cities = {}
    cities = {"Бобров": {"url_city": "bobrov"},
              "Борисоглебск": {"url_city": "borisoglebsk"},
              "Лиски": {"url_city": "liski"},
              "Нововоронеж": {"url_city": "novovoronezh"},
              "Семилуки": {"url_city": "semiluki"},
              "Бобровский район": {"url_city": "bobrovskiy-rayon"},
              "Борисоглебский городской округ": {"url_city": "borisoglebskiy-gorodskoy-okrug"},
              "Лискинский район": {"url_city": "liskinskiy-rayon"},
              "городской округ Нововоронеж": {"url_city": "gorodskoy-okrug-novovoronezh"},
              "Новоусманский район": {"url_city": "novousmanskiy-rayon"},
              "Рамонский район": {"url_city": "ramonskiy-rayon"},
              "Семилукский район": {"url_city": "semilukskiy-rayon"},
              "Хохольский район": {"url_city": "hoholskiy-rayon"}
              }
    cities_urls = {}
    cities_urls = {"Воронеж": {"url_city": "https://domostroyrf.ru/voronezh/novostroyki"}}
    for city, url in cities.items():
        cities_urls[city] = {"url_city": domain_cities + url["url_city"]}
    return cities_urls



cities = parse_cities()
for city, url_city in cities.items():
    zhks = domostroy.get_zhks_urls(url_city["url_city"])
    for zhk, url_zhk in zhks.items():
        buildings = domostroy.get_buildings_urls(url_zhk)
        for building, url_building in buildings.items():
            apartments = domostroy.get_building_data(url_building)
            buildings[building] = apartments
        zhks[zhk] = buildings
    cities[city] = zhks

for city, city_data in cities.items():
    domostroy.save_to_xlsx(city, city_data)
print("All done!")
