from dataclasses import asdict, dataclass
from typing import List, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    Message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.Message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # один шаг
    M_IN_KM: float = 1000  # константа для перевода м. в км.
    HOURS_IN_MINUTES: float = 60  # минуты в час

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
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18  # первая константа для расчёта
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79  # вторая константа для расчёта

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.HOURS_IN_MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    MULTIPLIER_CALORIES_1: float = 0.035  # множитель для расчёта
    MULTIPLIER_CALORIES_2: float = 0.029  # множитель для расчёта
    KMHOUR_IN_MSECOND: float = 0.278  # перевод км.ч в м
    SM_IN_MTR: float = 100  # сантиметров в метре

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.MULTIPLIER_CALORIES_1 * self.weight
                + ((self.get_mean_speed() * self.KMHOUR_IN_MSECOND)**2
                 / (self.height / self.SM_IN_MTR))
                 * self.MULTIPLIER_CALORIES_2 * self.weight)
                * (self.duration * self.HOURS_IN_MINUTES))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # один гребок
    MULTIPLIER_CALORIES_3: float = 1.1  # множитель для расчёта
    MULTIPLIER_CALORIES_4: float = 2  # множитель для расчёта

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.MULTIPLIER_CALORIES_3)
                * self.MULTIPLIER_CALORIES_4 * self.weight * self.duration)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                 'RUN': Running,
                                                 'WLK': SportsWalking}
    if workout_type not in training_types:
        raise ValueError("Несуществующий тип тренировки")
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
