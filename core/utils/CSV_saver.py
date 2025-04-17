import os
import pandas as pd
from core.config import FILENAME_TEMPLATE, RESULTS_DIR


"""   Реализация сохранения результатов в формате CSV.   """

class CSVSaver:
    """Класс для сохранения отзывов в csv."""

    @staticmethod
    def save_to_CSV(reviews, product_ids):
        """Сохраняет отзывы в файл csv."""
        if not reviews:
            print("Нет отзывов для сохранения.")
            return

        # Создание пути файла
        os.makedirs(RESULTS_DIR, exist_ok=True)
        # Созднание имя файла
        filename = FILENAME_TEMPLATE.format(product_ids)
        # Создание названия пути файла
        filepath = os.path.join(RESULTS_DIR, filename)

        # Создает датасет с результатами парсинга
        pd.DataFrame(reviews).to_csv(filepath, index=False)
        print(f"Данные сохранены в {filepath}")