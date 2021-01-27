import domostroy

def parse_cities():

    domain = "https://www.domostroynn.ru"
    domain_cities = domain + "/novostroyki/nizhegorodskaya-oblast/"
    cities = {}
    cities = {"Азамас": {"url_city": "arzamas"},
              "Балахна": {"url_city": "balahna"},
              "Бор": {"url_city": "bor"},
              "Городец": {"url_city": "gorodec"},
              "Дзержинск": {"url_city": "dzerzhinsk"},
              "Кстово": {"url_city": "kstovo"},
              "городской округ Арзамас": {"url_city": "gorodskoy-okrug-arzamas"},
              "Балахнинский район": {"url_city": "balahninskiy-rayon"},
              "Богородский район": {"url_city": "bogorodskiy-rayon"},
              "городской округ Бор": {"url_city": "bogorodskiy-rayon"},
              "Городецкий район": {"url_city": "gorodeckiy-rayon"},
              "городской округ Дзержинск": {"url_city": "gorodskoy-okrug-dzerzhinsk"},
              "Кстовский район": {"url_city": "kstovskiy-rayon"}
              }
    cities_urls = {}
    cities_urls = {"Нижний Новгород": {"url_city": "https://www.domostroynn.ru/novostroyki"}}
    for city, url in cities.items():
        cities_urls[city] = {"url_city": domain_cities + url["url_city"]}
    return cities_urls


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
