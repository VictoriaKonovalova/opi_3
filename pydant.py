#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Использовать словарь, содержащий следующие ключи: название пункта назначения; номер
поезда; время отправления. Написать программу, выполняющую следующие действия:
ввод с клавиатуры данных в список, состоящий из словарей заданной структуры; записи должны
быть упорядочены по номерам поездов;
вывод на экран информации о поезде, номер которого введен с клавиатуры; если таких поездов нет,
выдать на дисплей соответствующее сообщение.
"""

import sys
import json
from pydantic import BaseModel, ValidationError, validator


class TrainSchema(BaseModel):
    name: str
    num: int
    time: str


def add(trains, name, num, time):
    # Создать словарь
    train = {
        'name': name,
        'num': num,
        'time': time,
    }

    trains.append(train)
    if len(trains) > 1:
        trains.sort(key=lambda item: item.get('num', ''))


def listt(trains):
    """
        Отобразить список маршрутов
    """
    if trains:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 17
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^17} |'.format(
                "№",
                "Пункт назначения",
                "Номер поезда",
                "Время отправления"
            )
        )
        print(line)
        # Вывести данные о всех маршрутах
        for idx, train in enumerate(trains, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>17} |'.format(
                    idx,
                    train.get('name', ''),
                    train.get('num', ''),
                    train.get('time', 0)
                )
            )

        print(line)
    else:
        print("Список маршрутов пуст!")


def select_train(trains, number):
    """""
    Выбрать маршруты с заданным номер поезда
    """""
    # Сформировать список поездов
    result = []
    for rattler in trains:
        if rattler.get('num') == number:
            result.append(rattler)

    # Возвратить список выбранных маршрутов
    return result


def save(file_name, route):
    with open(file_name, 'w') as fout:
        json.dump(route, fout)


def load(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        indata = json.load(fin)
        try:
            for i in indata:
                TrainSchema.parse_raw(str(i).replace("'", '"'))
            print("Validation was successful")
            return indata
        except ValidationError as err:
            print("Error in validation")
            print(err)


def main():
    """
        Главная функция программы
    """
    # Сформировать список маршрутов
    route = []

    # Организовать бесконечный цикл запроса команд
    while True:
        command = input(">>> ").lower()

        if command == 'exit':
            break

        elif command == 'add':
            name = input("Название пункта назначения: ")
            num = int(input("Номер поезда: "))
            time = input("Время отправления: ")

            add(route, name, num, time)

        elif command == 'list':
            listt(route)

        elif command.startswith('select '):
            parts = command.split(' ', maxsplit=1)
            number = int(parts[1])
            selected = select_train(route, number)
            listt(selected)

        elif command.startswith('load '):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            route = load(file_name)

        elif command.startswith('save '):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save(file_name, route)

        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить поезд;")
            print("list - вывести список поездов;")
            print("select <номер поезда> - запросить информацию о выбранном поезде;")
            print("load <имя_файла> - загрузить данные из файла;")
            print("save <имя_файла> - сохранить данные в файл;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
