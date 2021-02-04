import domostroy
import domostroy_query_zhk
import domostroy_query_building

cities = domostroy.get_site_urls()
domostroy.print_cities_table(cities)

try:
    key_city = int(input("Введите номер города или соответствующий п. меню для парсинга данных: "))
    if key_city not in cities.keys() and key_city not in [101, 102]:
        print("Нет такого п. меню в списке!")
        quit()
except:
    print("Нет такого п. меню в списке!")
    quit()

if key_city in cities.keys():
    print("Processing...")
    city_name, city_url = cities[key_city]
    city_main_url = domostroy.get_city_main_url(city_url)
    cities = domostroy.get_cities_names_urls(city_name, city_main_url)
    for city, url_city in cities.items():
        zhks = domostroy.get_zhks_urls(url_city["url_city"], url_zhks={}, params={})
        for zhk, url_zhk in zhks.items():
            buildings = domostroy.get_buildings_urls(url_zhk)
            for building, url_building in buildings.items():
                apartments = domostroy.get_building_data(url_building, dict_apartments={}, params={}, aptmt=1)
                buildings[building] = apartments
            zhks[zhk] = buildings
        cities[city] = zhks

    for city, city_data in cities.items():
        domostroy.save_to_xlsx(city, city_data)
    print()
    print("All done!")

elif key_city == 101:
    domostroy_query_zhk.query_zhk()
elif key_city == 102:
    domostroy_query_building.query_building()
