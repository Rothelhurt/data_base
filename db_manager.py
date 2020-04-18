from collections import Counter


class DataBaseManager:
    """
    Класс для управления базой.
    """
    def __init__(self):
        self.db = {}
        self.END = False
        self.functions = {
            'SET': self.set_val,
            'GET': self.get,
            'UNSET': self.unset,
            'COUNTS': self.counts,
            'END': self.end,
            'BEGIN': self.begin,
            'COMMIT': self.commit,
            'ROLLBACK': self.rollback,
            }

    def set_val(self, *args):
        """Устанавилвает значение."""
        self.db[args[0]] = args[1]

    def get(self, *args):
        """Выводит значение по ключу на экран."""
        key = args[0]
        if key in self.db:
            print(self.db[key])
        else:
            print('NULL')

    def unset(self, *args):
        """Удаляет значение по ключу из базы."""
        key = args[0]
        if key in self.db:
            self.db.pop(key)
        else:
            print(key, 'IS NOT DEFINED')

    def counts(self, *args):
        """Показывает сколько раз данное значение встречается в базе данных."""
        counter = Counter(self.db.values())
        value = args[0]
        print(counter[value])

    def end(self):
        """Завершает работу."""
        self.END = True

    def begin(self):
        """Начинает транзакцию."""
        # Создание объекта транзакции.
        transaction = Transaction()
        # Если транзакция завершилась вызовом commit(),
        # a не rollback(), применяем изменение базы данных,
        # вызываем commit() у класс-родителя.
        if transaction.run() != {}:
            self.db.update(transaction.run())
            self.commit()

    def commit(self):
        """В базовом классе ничего не делает."""
        pass

    def rollback(self):
        """В базовом классе ничего не делает."""
        pass

    def run(self):
        """Запускает приложение."""
        while not self.END:
            command = list(input().split())
            self.pars_command(command)
        return self.db

    def pars_command(self, command):
        if len(command) == 1:
            self.functions[command[0].upper()]()
        elif len(command) >= 2:
            self.functions[command[0].upper()](*command[1:])


class Transaction(DataBaseManager):
    """Класс для управления транзакцией."""

    def commit(self):
        """Завершает транзакцию."""
        self.end()

    def rollback(self):
        """Отменяет изменения в транзакции и завершает транзакцию."""
        self.db = {}
        self.end()


db_manager = DataBaseManager()
db_manager.run()
