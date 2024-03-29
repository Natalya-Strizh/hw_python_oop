
from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFORMATIOON = ('Тип тренировки: {}; '
                    'Длительность: {:.3f} ч.; '
                    'Дистанция: {:.3f} км; '
                    'Ср. скорость: {:.3f} км/ч; '
                    'Потрачено ккал: {:.3f}.')

    def get_message(self) -> None:
        mes = asdict(self)
        return self.INFORMATIOON.format(*mes.values())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return NotImplementedError('не получилось рассчитать каллории')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_3: float = 0.035
    COEFF_CALORIE_4: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_3 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_4 * self.weight)
                * self.duration * self.H_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_5: float = 1.1
    COEFF_CALORIE_6: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CALORIE_5)
                * self.COEFF_CALORIE_6 * self.weight)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_dict.keys():
        return training_dict[workout_type](*data)
    else:
        raise ValueError('Тип тренировки не найден')


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print_message = info.get_message()
    print(print_message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [1500, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

# Здравствуйте! Спасибо большое за объяснения и статью!
# У меня только вопрос по поводу констант.
# В прошлой итерации у меня константы были в дочернем классе.
# Мне необходимо было вынести на уровень класса по аналогии с LEN_STEP.
# Я сделала вывод что нужно в родительский класс и вынесла.
# Возможно я Вас неверно поняла.
# Конечно специфические константы долджны быть каждый в своём классе.
# Про обработку ошибок и более сложные аннотации записала
# в свой конспект. Спасибо!