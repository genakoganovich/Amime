import csv
import json
from typing import List, Dict
from dataclasses import dataclass
from motion.actor_configuration import ActorConfigurationBuilder


@dataclass
class ActorConfigRow:
    """Строка конфигурации"""
    actor_type: str
    color: str
    interpolation_type: str


class ActorLoader:
    """Загрузчик конфигурации акторов"""

    @staticmethod
    def load_from_csv(filepath: str, global_params: Dict) -> tuple:
        """Загрузить из CSV (табуляция)"""
        rows = ActorLoader._read_csv(filepath)
        return ActorLoader._build_config(rows, global_params)

    @staticmethod
    def _read_csv(filepath: str) -> List[ActorConfigRow]:
        """Прочитать CSV с автоматическим определением колонок"""
        rows = []

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')

            # Выводим заголовки для отладки
            if reader.fieldnames:
                print(f"Найденные колонки: {reader.fieldnames}")

            for row in reader:
                try:
                    # Пытаемся найти нужные колонки (с разными вариантами названий)
                    actor_type = ActorLoader._get_value(row, ['actor', 'actor_type', 'type'])
                    color = ActorLoader._get_value(row, ['color', 'Color'])
                    interp_type = ActorLoader._get_value(row, ['interpolation_type', 'interpolation', 'method', 'type'])

                    if not all([actor_type, color, interp_type]):
                        print(f"Пропускаем строку (неполные данные): {row}")
                        continue

                    rows.append(ActorConfigRow(
                        actor_type=actor_type.strip(),
                        color=color.strip(),
                        interpolation_type=interp_type.strip()
                    ))
                except Exception as e:
                    print(f"Ошибка при чтении строки: {e}")
                    continue

        if not rows:
            raise ValueError(f"Не найдены валидные строки в файле {filepath}")

        return rows

    @staticmethod
    def _get_value(row: dict, possible_keys: List[str]) -> str:
        """Получить значение из словаря по одному из возможных ключей"""
        for key in possible_keys:
            if key in row:
                return row[key]
        return None

    @staticmethod
    def load_from_json(filepath: str, global_params: Dict) -> tuple:
        """Загрузить из JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        rows = [
            ActorConfigRow(
                actor_type=item['actor'],
                color=item['color'],
                interpolation_type=item['interpolation_type']
            )
            for item in data['actors']
        ]

        return ActorLoader._build_config(rows, global_params)

    @staticmethod
    def _build_config(rows: List[ActorConfigRow], global_params: Dict) -> tuple:
        """Построить конфигурацию из строк"""
        actor_config = ActorConfigurationBuilder(global_params)
        animation_config = {}

        for idx, row in enumerate(rows):
            actor_name = f"{row.actor_type}_{row.color}_{idx}"

            if row.actor_type.lower() == "sphere":
                actor_config.add_sphere(actor_name, color=row.color)
            elif row.actor_type.lower() == "arrow":
                actor_config.add_arrow(actor_name, color=row.color)
            else:
                raise ValueError(f"Unknown actor type: {row.actor_type}")

            animation_config[actor_name] = row.interpolation_type

        return actor_config, animation_config