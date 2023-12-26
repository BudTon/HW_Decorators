import os
from functools import wraps
from datetime import datetime


def logger(path):

    def write_file(name_file, date):
        with open(f'{name_file}', 'a', encoding='utf8') as fa:
            fa.write(date)

    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            write_file(path,f'{datetime.now()} - дату и время вызова функции\n')
            write_file(path,f'{old_function.__name__} - имя функции\n')
            write_file(path,f'{args},{kwargs} - аргументы, с которыми вызвалась\n')
            result = old_function(*args, **kwargs)
            write_file(path,f'{result} - возвращаемое значение\n')
            write_file(path,f'\n')
            return result

        return new_function

    return __logger


def test_3(numbers_test):
    paths = []
    for i in range(numbers_test):
        path = f'log_task_3_test_{i+1}.log'
        paths.append(path)
    print(paths)

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def flat_generator(list_of_lists_2):
            for item in list_of_lists_2:
                if type(item) != list:
                    yield item
                else:
                    yield from flat_generator(item)

        @logger(path)
        def test_old():
            test_list = []

            list_of_lists_2 = [
                [['a'], ['b', 'c']],
                ['d', 'e', [['f'], 'h'], False],
                [1, 2, None, [[[[['!']]]]], []]
            ]

            for flat_iterator_item in flat_generator(list_of_lists_2):
                test_list.append(flat_iterator_item)




            print(test_list)

            return test_list
        result = test_old()

if __name__ == '__main__':
    numbers_test = int(input('Введите количество тестов:'))
    test_3(numbers_test)
