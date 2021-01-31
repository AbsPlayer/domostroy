import domostroy
# TODO: пейджинг
# TODO: меню выбора парсинга по ЖК и зданию. Предварительно очищая экран с основным меню

cities = domostroy.get_site_urls()
domostroy.print_cities_table(cities)

key_city = int(input("Введите номер города для парсинга данных: "))
if key_city not in cities.keys():
    print("Нет такого города в списке!")
    quit()
city_name, city_url = cities[key_city]

# city_url = "https://www.domostroydon.ru" # для теста
# city_name = "Ростов" # для теста
city_main_url = domostroy.get_city_main_url(city_url)
cities = domostroy.get_cities_names_urls(city_name, city_main_url)
for city, url_city in cities.items():
    zhks = domostroy.parse_zhks(url_city["url_city"])
    for zhk, url_zhk in zhks.items():
        buildings = domostroy.parse_buildings(url_zhk)
        for building, url_building in buildings.items():
            apartments = domostroy.parse_building(url_building)
            buildings[building] = apartments
        zhks[zhk] = buildings
    cities[city] = zhks

for city, city_data in cities.items():
    domostroy.save_to_xlsx(city, city_data)
print("All done!")
