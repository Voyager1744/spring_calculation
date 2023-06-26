from typing import Tuple


def get_gross_vehicle_weight(
        weight_on_front_axle: int,
        weight_on_back_axle: int) -> int:
    """ Получить полную массу автомобиля """

    return weight_on_front_axle + weight_on_back_axle


def get_unsprung_mass(axle_weight_front: int,
                      axle_weight_back: int,
                      wheel_weight_front: int,
                      wheel_weight_back: int
                      ) -> int:
    """ Получить неподрессоренную массу автомобиля """

    return (axle_weight_back +
            axle_weight_front +
            (wheel_weight_back * 2) +
            (wheel_weight_front * 2))


def get_weight_distribution(gross_weight: int,
                            axle_weight: int) -> float:
    """ Получить развесовку в % """

    return axle_weight / (gross_weight / 100)


def get_unsprung_mass_axle(
        axle_weight: int,
        wheel_weight: int) -> int:
    """ Получить неподрессоренную массу моста (кг)"""

    return axle_weight + wheel_weight * 2


def get_draught(
        spring_stroke: int,
        draught_in_percent: int
) -> float:
    """ Получить осадку в мм """

    return spring_stroke / 100 * draught_in_percent


def get_weight_of_suspension_strut(
        axle_weight: int,
        unspring_mass_axle: int
) -> float:
    """ Получить массу на стойку (кг) """

    return (axle_weight - unspring_mass_axle) / 2


# -------- Детальный расчет жесткости пружин ---------------------

# -------- Жесткость пружин стойки суммарная(Н/см) ---------------

def get_stiffness_of_suspension_summ(
        draught: float,
        weight_of_suspension_strut: float) -> float:
    """ Получить жесткость пружин стойки суммарная (Н/см) """

    return (weight_of_suspension_strut / draught) * 10


# -------- Жесткость пружин -----------

def get_stiffness_top_spring(
        stiffness_summ: float) -> float:
    """ Получить жесткость верхней пружины (Н/см) """

    return 12 * stiffness_summ / 7


def get_stiffness_bottom_spring(
        stiffness_top_spring: float) -> float:
    """ Получить жесткость нижней пружины (Н/см) """

    return stiffness_top_spring * 1.4
