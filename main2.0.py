from pymongo import MongoClient

# Параметры подключения
mongodb_host = "localhost"
mongodb_port = 27017
mongodb_username = "andrey"
mongodb_password = "2005"
mongodb_database = "laba"

try:
    # Создание URI подключения
    if mongodb_username and mongodb_password:
        connection_string = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_host}:{mongodb_port}/{mongodb_database}?authSource=admin"
    else:
        connection_string = f"mongodb://{mongodb_host}:{mongodb_port}/"

    # Создание клиента MongoClient
    client = MongoClient(connection_string)

    # Проверка подключения (пинг)
    client.admin.command('ping')
    print("Подключение к MongoDB успешно установлено!")

    # Получение доступа к базе данных
    db = client[mongodb_database]

except Exception as e:
    print(f"Ошибка подключения к MongoDB: {e}")


# Функция создания и заполнения коллекции
def create_and_fill_collection(collection, data):
    collection.insert_many(data)
    print("Коллекция создана и заполнена.")


# Функция вывода содержимого коллекции
def display_collection(collection):
    print("Содержимое коллекции:")
    for document in collection.find():
        print(document)


# Функция обновления записи по условию
def update_record(collection, condition, new_values):
    result = collection.update_many(condition, {"$set": new_values})
    if result.modified_count > 0:
        print(f"Обновлено {result.modified_count} записей.")
    else:
        print("Запись не найдена для обновления.")


# Функция удаления записи по условию
def delete_record(collection, condition):
    result = collection.delete_many(condition)
    if result.deleted_count > 0:
        print(f"Удалено {result.deleted_count} записей.")
    else:
        print("Запись не найдена для удаления.")


# Функция очистки коллекции
def clear_collection(collection):
    result = collection.delete_many({})
    print(f"Коллекция очищена. Удалено {result.deleted_count} записей.")


def main():
    collection_name = input("Введите название коллекции: ")
    number_of_records = int(input("Введите количество записей: "))

    collection = db[collection_name]

    # Ввод данных
    data = []
    for _ in range(number_of_records):
        record = input("Введите запись в формате name, phone, address, date_of_birth ")
        name, phone, address, date_of_birth = record.split(',')
        data.append({
            "name": name.strip(),
            "phone": phone.strip(),
            "address": address.strip(),
            "date_of_birth": date_of_birth.strip(),
        })

    create_and_fill_collection(collection, data)

    while True:
        print("\nВыберите операцию:")
        print("1. Вывести содержимое коллекции")
        print("2. Обновить запись")
        print("3. Удалить запись")
        print("4. Очистить коллекцию")
        print("5. Выход")

        choice = input("Введите номер операции: ")

        if choice == "1":
            display_collection(collection)
        elif choice == "2":
            # Пример: обновить номер телефона пользователя по имени
            name_to_update = input("Введите имя пользователя для обновления: ")
            new_phone = input("Введите новый номер телефона: ")
            condition = {"name": name_to_update}
            new_values = {"phone": new_phone}
            update_record(collection, condition, new_values)
        elif choice == "3":
            # Пример: удалить пользователя по имени
            name_to_delete = input("Введите имя пользователя для удаления: ")
            condition = {"name": name_to_delete}
            delete_record(collection, condition)
        elif choice == "4":
            clear_collection(collection)
        elif choice == "5":
            return False
        else:
            print("Неверный ввод. Пожалуйста, выберите операцию из списка.")


if __name__ == "__main__":
    main()