import domostroy

def query_zhk():
    city_name = input("Введите название города: ") # город
    zhk_name = input("Введите название ЖК: ") # название ЖК
    url_zhk = input("Введите ссылку на ЖК: ") # ссылка на ЖК
    # все введенные данные будут использованы в xls-отчёте

    cities = {}
    zhks = {}
    buildings = {}
    print("Processing...")
    buildings = domostroy.get_buildings_urls(url_zhk)
    for building, url_building in buildings.items():
        apartments = domostroy.get_building_data(url_building, dict_apartments={}, params={}, aptmt=1)
        buildings[building] = apartments
    zhks[zhk_name] = buildings
    cities[city_name] = zhks

    for city, city_data in cities.items():
        domostroy.save_to_xlsx(city, city_data, zhk_name_manual=zhk_name)

    print("All done!")
