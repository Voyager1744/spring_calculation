class Springs:
    """ Модель пружины. """

    def __init__(self,
                 front_axle: int = 780,  # Вес на оси (кг)
                 back_axle: int = 620,  # Вес на оси (кг)
                 not_sus_axle_front: int = 130,  # Вес моста
                 not_sus_axle_back: int = 110,  # Вес моста
                 wheel_front: int = 40,  # Вес колеса
                 wheel_back: int = 40,  # Вес колеса
                 spring_stroke_front: int = 325,  # Ход стойки
                 spring_stroke_back: int = 325,  # Ход стойки
                 height_front: int = 800,  # Высота стойки
                 height_back: int = 800,  # Высота стойки
                 draught_in_percent_front: int = 50,  # Осадка в %
                 draught_in_percent_back: int = 50  # Осадка в %
                 ):
        self.front_axle = front_axle  # Вес на оси (кг)
        self.back_axle = back_axle  # Вес на оси (кг)
        self.not_sus_axle_front = not_sus_axle_front  # Вес моста
        self.not_sus_axle_back = not_sus_axle_back  # Вес моста
        self.wheel_front = wheel_front  # Вес колеса
        self.wheel_back = wheel_back  # Вес колеса
        self.spring_stroke_front = spring_stroke_front  # Ход стойки
        self.spring_stroke_back = spring_stroke_back  # Ход стойки
        self.height_front = height_front  # Высота стойки
        self.height_back = height_back  # Высота стойки
        self.draught_in_percent_front = draught_in_percent_front  # Осадка в %
        self.draught_in_percent_back = draught_in_percent_back  # Осадка в %

        # Полная масса автомобиля
        self.full_mass = front_axle + back_axle

        # Неподрессоренная масса (кг)
        self.full_mass_not_sus = sum(
            (self.not_sus_axle_front,
             self.not_sus_axle_back,
             self.wheel_front * 2,
             self.wheel_back * 2)
        )

        # Развесовка в %
        self.distribution_front = (
                self.front_axle / (self.full_mass / 100)
        )
        self.distribution_back = (
                100 - self.distribution_front
        )

        # Неподрессоренные массы (кг)
        self.not_sus_mass_axle_front = (
                self.not_sus_axle_front + self.wheel_front * 2
        )
        self.not_sus_mass_axle_back = (
                self.not_sus_axle_back + self.wheel_back * 2
        )

        # Осадка (мм)
        self.draught_front = (
                self.spring_stroke_front / 100 * self.draught_in_percent_front
        )
        self.draught_back = (
                self.spring_stroke_back / 100 * self.draught_in_percent_back
        )

        # Масса на стойку (кг)
        self.mass_on_strut_front = (
                (self.front_axle - self.not_sus_mass_axle_front) / 2
        )
        self.mass_on_strut_back = (
                (self.back_axle - self.not_sus_mass_axle_back) / 2
        )

        # Жесткость пружин стойки суммарная (Н/см)
        self.stiff_summ_front_exact = (  # Точная
                (self.mass_on_strut_front / self.draught_front) * 10
        )
        self.stiff_summ_front_round = (  # Округленная
            int(self.stiff_summ_front_exact)
        )

        self.stiff_summ_back_exact = (  # Точная
                (self.mass_on_strut_back / self.draught_back) * 10
        )
        self.stiff_summ_back_round = (  # Округленная
            int(self.stiff_summ_back_exact)
        )

        # Жесткость передних пружин (Н/см)

        self.stiff_front_top_exact = (  # Верхняя пружина точная
                12 * self.stiff_summ_front_exact / 7
        )
        self.stiff_front_top_round = (  # Верхняя пружина округленная
            int(self.stiff_front_top_exact)
        )
        self.stiff_front_top_cat = (  # Верхняя пружина каталожная
                (self.stiff_front_top_round // 5) * 5
        )

        self.stiff_front_bottom_exact = (  # Нижняя пружина точная
                self.stiff_front_top_exact * 1.4
        )
        self.stiff_front_bottom_round = (  # Нижняя пружина округленная
            int(self.stiff_front_bottom_exact)
        )
        self.stiff_front_bottom_cat = (  # Нижняя пружина каталожная
                (self.stiff_front_bottom_round // 5) * 5
        )

        # Жесткость задних пружин (Н/см)

        self.stiff_back_top_exact = (  # Верхняя пружина точная
                12 * self.stiff_summ_back_exact / 7
        )
        self.stiff_back_top_round = (  # Верхняя пружина округленная
            int(self.stiff_back_top_exact)
        )
        self.stiff_back_top_cat = (  # Верхняя пружина каталожная
                (self.stiff_back_top_round // 5) * 5
        )

        self.stiff_back_bottom = (  # Нижняя пружина точная
                self.stiff_back_top_exact * 1.4
        )
        self.stiff_back_bottom_round = (  # Нижняя пружина округленная
            int(self.stiff_back_bottom)
        )
        self.stiff_back_bottom_cat = (  # Нижняя пружина каталожная
                (self.stiff_back_bottom_round // 5) * 5
        )

        # Жесткость передней стойки суммарная (Н/см) Каталог
        self.stiff_summ_front_cat = int(
            (self.stiff_front_top_cat * self.stiff_front_bottom_cat) /
            (self.stiff_front_top_cat + self.stiff_front_bottom_cat)
        )
        # Жесткость задней стойки суммарная (Н/см) Каталог
        self.stiff_summ_back_cat = int(
            (self.stiff_back_top_cat * self.stiff_back_bottom_cat) /
            (self.stiff_back_top_cat + self.stiff_back_bottom_cat)
        )

    def get_summary_data(self):
        """ Сводные данные """

        return {
            "Полная мааса автомобиля(кг)": self.full_mass,
            "Неподрессоренная масса (кг)": self.full_mass_not_sus,
            "Передние пружины верхняя (Н/мм)": self.stiff_front_top_cat,
            "Передние пружины нижняя (Н/мм)": self.stiff_front_bottom_cat,
            "Задние пружины верхняя (Н/мм)": self.stiff_back_top_cat,
            "Задние пружины нижняя (Н/мм)": self.stiff_back_bottom_cat
        }

    def get_calculation_of_spring_stiffness(self):
        """ Детальный расчет жесткости пружин. """

        context = {
            "Жесткость пружин стойки суммарная (Н/см)": {
                "Передняя": {
                    "точная": self.stiff_summ_front_exact,
                    "округленная": self.stiff_summ_front_round,
                    "каталожная": self.stiff_summ_front_cat,
                },
                "Задняя": {
                    "точная": self.stiff_summ_back_exact,
                    "округленная": self.stiff_summ_back_round,
                    "каталожная": self.stiff_summ_back_cat
                }

            },
            "Жесткость передних пружин (Н/см)": {
                "Верхняя": {
                    "точная": self.stiff_front_top_exact,
                    "округленная": self.stiff_front_top_round,
                    "каталожная": self.stiff_front_top_cat
                },
                "Нижняя": {
                    "точная": self.stiff_front_bottom_exact,
                    "округленная": self.stiff_front_bottom_round,
                    "каталожная": self.stiff_front_bottom_cat
                }
            },
            "Жесткость задних пружин (Н/см)": {
                "Верхняя": {
                    "точная": self.stiff_back_top_exact,
                    "округленная": self.stiff_back_top_round,
                    "каталожная": self.stiff_back_top_cat
                },
                "Нижняя": {
                    "точная": self.stiff_back_bottom,
                    "округленная": self.stiff_back_bottom_round,
                    "каталожная": self.stiff_back_bottom_cat
                }
            }

        }
        return context


def main():
    s = Springs()

    print(s.full_mass)
    print(s.full_mass_not_sus)

    print(f"{s.distribution_front:.5f}", f"{s.distribution_back:.5f}")
    print(s.draught_front, s.draught_back)
    print(s.mass_on_strut_front, s.mass_on_strut_back)

    for i in s.get_summary_data():
        print(f"{i}: {s.get_summary_data()[i]}")

    for i in s.get_calculation_of_spring_stiffness():
        print(f"{i}: {s.get_calculation_of_spring_stiffness()[i]}")


if __name__ == "__main__":
    main()
