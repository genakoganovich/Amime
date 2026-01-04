Amime/
├── motion/
│   ├── __init__.py
│   ├── trajectory.py       # функции: polyline_length, cumulative_lengths
│   ├── kinematics.py       # (пока пусто) расчеты движения объектов
│   ├── geometry.py         # (пока пусто) геометрические функции
│   └── speed.py            # (пока пусто) расчеты скорости движения камеры/объекта
│
├── tests/
│   ├── test_trajectory.py  # тесты для polyline_length и cumulative_lengths
│   ├── test_kinematics.py  # заглушка
│   └── test_speed.py        # заглушка
│
├── visual/
│   ├── plot_trajectory.py       # matplotlib визуализация траектории
│   ├── plot_polyline_pyvista.py # PyVista визуальный тест траектории + шар
│   ├── plot_polyline_vista_cam_2.py # PyVista два окна, камера статичная + следящая
│   └── chase_demo.py             # (будет) демонстрация камеры с разными поведениями
│
├── main.py            # временный скрипт для экспериментов
├── pyproject.toml     # настройки pytest и окружения
└── README.md

| Модуль                              | Состояние    | Комментарий                                                                   |
| ----------------------------------- | ------------ | ----------------------------------------------------------------------------- |
| motion/trajectory.py                | Готов        | Реализованы polyline_length и cumulative_lengths, протестировано              |
| motion/kinematics.py                | В разработке | План: функции расчета скорости, ускорения и траекторий движения камеры        |
| motion/geometry.py                  | В разработке | План: функции для векторов, углов, направлений камеры                         |
| motion/speed.py                     | В разработке | План: расчеты скорости для разных поведения камер (Follow, Ambush, FastOrbit) |
| tests/test_trajectory.py            | Готов        | Покрывает polyline_length и cumulative_lengths                                |
| tests/test_kinematics.py            | Заглушка     | Тесты будут добавлены после реализации kinematics                             |
| tests/test_speed.py                 | Заглушка     | Тесты будут добавлены после реализации speed                                  |
| visual/plot_trajectory.py           | Готов        | Визуализация траектории через matplotlib                                      |
| visual/plot_polyline_pyvista.py     | Готов        | PyVista визуализация траектории + шар                                         |
| visual/plot_polyline_vista_cam_2.py | Готов        | PyVista два окна: статичная камера + следящая камера                          |
| visual/chase_demo.py                | В разработке | Демонстрация поведения камер (Follow, Ambush, TiredChase, FastOrbit)          |

