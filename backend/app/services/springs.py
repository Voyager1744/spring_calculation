from backend.app.services import funcs


class Auto:

    def __init__(self,
                 weight_on_front_axle: int,
                 weight_on_back_axle: int,
                 weight_not_sus_axle_front: int,
                 weight_not_sus_axel_back: int,
                 weight_wheel_front: int,
                 weight_wheel_back: int,
                 spring_stroke_front: int,
                 spring_stroke_back: int,
                 draught_in_percent_front: int,
                 draught_in_percent_back: int
                 ):
        self.weight_on_front_axle = weight_on_front_axle
        self.weight_on_back_axle = weight_on_back_axle
        self.weight_not_sus_axle_front = weight_not_sus_axle_front
        self.weight_not_sus_axel_back = weight_not_sus_axel_back
        self.weight_wheel_front = weight_wheel_front
        self.weight_wheel_back = weight_wheel_back
        self.spring_stroke_front = spring_stroke_front
        self.spring_stroke_back = spring_stroke_back
        self.draught_in_percent_front = draught_in_percent_front
        self.draught_in_percent_back = draught_in_percent_back


class Springs(Auto):
    def __init__(self,
                 weight_on_front_axle: int,
                 weight_on_back_axle: int,
                 weight_not_sus_axle_front: int,
                 weight_not_sus_axel_back: int,
                 weight_wheel_front: int,
                 weight_wheel_back: int,
                 spring_stroke_front: int,
                 spring_stroke_back: int,
                 draught_in_percent_front: int,
                 draught_in_percent_back: int
                 ):
        super().__init__(
            weight_on_front_axle,
            weight_on_back_axle,
            weight_not_sus_axle_front,
            weight_not_sus_axel_back,
            weight_wheel_front,
            weight_wheel_back,
            spring_stroke_front,
            spring_stroke_back,
            draught_in_percent_front,
            draught_in_percent_back,
        )
        # Полная масса автомобиля
        self.full_mass = funcs.get_gross_vehicle_weight(
            weight_on_front_axle, weight_on_back_axle
        )

        # Развесовка в %
        self.weight_distribution_front = funcs.get_weight_distribution(
            self.full_mass,
            self.weight_on_front_axle)

        self.weight_distribution_back = funcs.get_weight_distribution(
            self.full_mass,
            self.weight_on_back_axle)

        # Неподрессоренная масса (кг)
        self.unsprung_mass_axle_front = funcs.get_unsprung_mass_axle(
            self.weight_not_sus_axle_front, self.weight_wheel_front
        )

        self.unsprung_mass_axle_back = funcs.get_unsprung_mass_axle(
            self.weight_not_sus_axel_back, self.weight_wheel_back
        )

        # Осадка (мм)
        self.draught_front = funcs.get_draught(
            self.spring_stroke_front, self.draught_in_percent_front
        )

        self.draught_back = funcs.get_draught(
            self.spring_stroke_back, self.draught_in_percent_back
        )

        # Масса на стойку (кг)
        self.weight_of_suspension_strut_front = (
            funcs.get_weight_of_suspension_strut(
                self.weight_on_front_axle,
                self.unsprung_mass_axle_front
            )
        )

        self.weight_of_suspension_strut_back = (
            funcs.get_weight_of_suspension_strut(
                self.weight_on_back_axle,
                self.unsprung_mass_axle_back
            )
        )


def main():
    test_params = {
        'weight_on_front_axle': 780,
        'weight_on_back_axle': 620,
        'weight_not_sus_axle_front': 130,
        'weight_not_sus_axel_back': 110,
        'weight_wheel_front': 40,
        'weight_wheel_back': 40,
        'spring_stroke_front': 325,
        'spring_stroke_back': 325,
        'draught_in_percent_front': 50,
        'draught_in_percent_back': 50
    }
    a = Springs(**test_params)
    print(a.weight_distribution_front, a.weight_distribution_back)
    print(a.unsprung_mass_axle_front, a.unsprung_mass_axle_back)
    print(a.draught_front, a.draught_back)
    print(a.weight_of_suspension_strut_front, a.weight_of_suspension_strut_back)

    stiff_front = funcs.get_stiffness_of_suspension_summ(
        a.draught_front,
        a.weight_of_suspension_strut_front
    )
    stiff_back = funcs.get_stiffness_of_suspension_summ(
        a.draught_back,
        a.weight_of_suspension_strut_back
    )
    print(f'{stiff_front:.3f}', f'{stiff_back:.3f}')


main()
