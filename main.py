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
