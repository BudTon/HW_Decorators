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


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
