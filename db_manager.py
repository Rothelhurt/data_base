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
        if len(args) == 2:
            if args[1] == 'NULL':
                print('"NULL" IS AN UNACCEPTABLE VALUE. USE "UNSET" COMMAND')
            self.db[args[0]] = args[1]
        else:
            print('"SET" REQUIRES 2 ARGUMENTS.', len(args), 'WERE GIVEN.')

    def get(self, *args):
        """Выводит значение по ключу на экран."""
        if args:
            if len(args) == 1:
                key = args[0]
                if key in self.db:
                    print(self.db[key])
                else:
                    print('NULL')
            else:
                print('"GET" REQUIRES 1 ARGUMENT.')
        else:
            print('"GET" REQUIRES AN VARIABLE NAME.')

    def unset(self, *args):
        """Удаляет значение по ключу из базы."""
        if args:
            key = args[0]
            if key in self.db:
                self.db.pop(key)
        else:
            print('"UNSET" REQUIRES AN VARIABLE NAME.')

    def counts(self, *args):
        """Показывает сколько раз данное значение встречается в базе данных."""
        if args:
            counter = Counter(self.db.values())
            value = args[0]
            print(counter[value])
        else:
            print('ENTER VALUE TO COUNT.')

    def end(self, *args):
        """Завершает работу."""
        if args:
            print('"END" REQUIRES NO ARGUMENTS.')
        else:
            self.END = True

    def begin(self, *args):
        """Начинает транзакцию."""
        # Создание объекта транзакции.
        transaction = Transaction()
        # Если транзакция завершилась вызовом commit(),
        # a не rollback(), применяем изменение базы данных,
        # вызываем commit() у класс-родителя.
        if transaction.run() != {}:
            self.db.update(transaction.run())
            self.commit()

    def commit(self, *args):
        """В базовом классе ничего не делает."""
        pass

    def rollback(self, *args):
        """В базовом классе ничего не делает."""
        pass

    def run(self):
        """Запускает приложение."""
        while not self.END:
            command = list(input().split())
            self.pars_command(command)
        return self.db

    def pars_command(self, command):
        if command[0].upper() in self.functions.keys():
            if len(command) == 1:
                self.functions[command[0].upper()]()
            elif 2 <= len(command) <= 3:
                self.functions[command[0].upper()](*command[1:])
            else:
                print('SYNTAX ERROR IN:', *command)
        else:
            print('UNKNOWN COMMAND:', command[0].upper())


class Transaction(DataBaseManager):
    """Класс для управления транзакцией."""

    def commit(self, *args):
        """Завершает транзакцию."""
        if args:
            print('"COMMIT" REQUIRES NO ARGUMENTS.')
        else:
            self.END = True

    def rollback(self, *args):
        """Отменяет изменения в транзакции и завершает транзакцию."""
        if args:
            print('"ROLLBACK" REQUIRES NO ARGUMENTS.')
        else:
            self.db = {}
            self.END = True

    def unset(self, *args):
        if args:
            key = args[0]
            self.db[key] = 'NULL'
        else:
            print('"UNSET" REQUIRES AN VARIABLE NAME.')

    def end(self, *args):
        print('COMMIT OR ROLLBACK ALL TRANSACTIONS BEFORE EXIT.')


db_manager = DataBaseManager()
db_manager.run()
