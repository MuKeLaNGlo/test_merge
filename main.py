from dataclasses import dataclass, asdict
from typing import ClassVar, List
from typing_extensions import Final


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Функция вывода сообщения о тренировке."""
        message = (
            "Тип тренировки: {training_type}; "
            "Длительность: {duration:.3f} ч.; "
            "Дистанция: {distance:.3f} км; "
            "Ср. скорость: {speed:.3f} км/ч; "
            "Потрачено ккал: {calories:.3f}."
        )
        return message.format(
            **asdict(self)
        )


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: Final[float] = 1000
    MIN_IN_H: Final[float] = 60
    HOURS_IN_MIN: Final[float] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f"Определите get_spent_calories в {self.__class__.__name__}."
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.HOURS_IN_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KM_H_IN_M_H: float = 0.278
    CENTIMETERS_IN_M: float = 100

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight
            + (
                (self.get_mean_speed() * self.KM_H_IN_M_H) ** 2
                / (self.height / self.CENTIMETERS_IN_M)
            )
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
            * self.weight
        ) * (self.duration * self.HOURS_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT: Final[float] = 1.1
    CALORIES_MULTIPLIER: Final[float] = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_trainings = {"RUN": Running, "WLK": SportsWalking, "SWM": Swimming}
    try:
        training = type_trainings[workout_type](*data)
    except KeyError:
        print("Unknown workout type")
        return None
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("WLK", [9000, 1, 75, 180]),
        ("WLK", [9000, 1.5, 75, 180]),
        ("WLK", [3000.33, 2.512, 75.8, 180.1]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
