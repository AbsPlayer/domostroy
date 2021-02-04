import domostroy

def query_building():
    city_name = input("Введите название города: ") # город
    zhk_name = input("Введите название ЖК: ") # название ЖК
    building_name = input("Введите номер дома: ") # номер дома
    building_url = input("Введите ссылку на дом: ") # ссылка на дом
    # все введенные данные будут использованы в xls-отчёте

    cities = {}
    zhks = {}
    buildings = {}
    print("Processing...")
    apartments = domostroy.get_building_data(building_url, dict_apartments={}, params={}, aptmt=1)
    buildings[building_name] = apartments
    zhks[zhk_name] = buildings
    cities[city_name] = zhks

    for city, city_data in cities.items():
        domostroy.save_to_xlsx(city, city_data, zhk_name_manual=zhk_name)
    print("All done!")
