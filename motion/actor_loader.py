import csv
import json
from typing import List, Dict
from motion.actor_config_schema import ActorConfigRow
from motion.actor_configuration import ActorConfigurationBuilder


class ActorLoader:
    """Загрузчик конфигурации акторов с поддержкой расширяемых параметров"""

    # Определяем обязательные поля
    REQUIRED_FIELDS = {'actor', 'color', 'interpolation_type', 'orientation_type'}

    @staticmethod
    def load_from_json(filepath: str, global_params: Dict) -> tuple:
        """Загрузить из JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        rows = []
        for item in data['actors']:
            # Проверяем обязательные поля
            ActorLoader._validate_item(item)

            # Извлекаем обязательные поля
            row = ActorConfigRow(
                actor_type=item['actor'],
                color=item['color'],
                interpolation_type=item['interpolation_type'],
                orientation_type=item['orientation_type'],
                extra={k: v for k, v in item.items()
                       if k not in ActorLoader.REQUIRED_FIELDS}
            )
            rows.append(row)

        return ActorLoader._build_config(rows, global_params)

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

            if reader.fieldnames:
                print(f"Найденные колонки: {reader.fieldnames}")

            for row in reader:
                try:
                    # Получаем обязательные поля
                    actor_type = ActorLoader._get_value(row, ['actor', 'actor_type', 'type'])
                    color = ActorLoader._get_value(row, ['color', 'Color'])
                    interp_type = ActorLoader._get_value(row, ['interpolation_type', 'interpolation', 'method'])
                    orient_type = ActorLoader._get_value(row, ['orientation_type', 'orientation'])

                    if not all([actor_type, color, interp_type, orient_type]):
                        print(f"Пропускаем строку (неполные данные): {row}")
                        continue

                    # Остальные параметры идут в extra
                    extra = {k: v for k, v in row.items()
                             if k not in ['actor', 'actor_type', 'type', 'color', 'Color',
                                          'interpolation_type', 'interpolation', 'method',
                                          'orientation_type', 'orientation']}

                    rows.append(ActorConfigRow(
                        actor_type=actor_type.strip(),
                        color=color.strip(),
                        interpolation_type=interp_type.strip(),
                        orientation_type=orient_type.strip(),
                        extra=extra
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
            if key in row and row[key]:
                return row[key]
        return None

    @staticmethod
    def _validate_item(item: Dict) -> None:
        """Проверить наличие обязательных полей"""
        missing = ActorLoader.REQUIRED_FIELDS - set(item.keys())
        if missing:
            raise ValueError(f"Отсутствуют обязательные поля: {missing}")

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

            # Сохраняем всю конфигурацию актора
            animation_config[actor_name] = row

        return actor_config, animation_config