import os
import time
import pandas as pd
from core.config import FILENAME_TEMPLATE, RESULTS_DIR


class ExcelSaver:
    """Класс для сохранения отзывов в csv."""

    @staticmethod
    def save_to_excel(reviews, product_ids):
        """Сохраняет отзывы в файл csv."""
        if not reviews:
            print("Нет отзывов для сохранения.")
            return

        os.makedirs(RESULTS_DIR, exist_ok=True)
        #product_ids_str = product_ids
        filename = FILENAME_TEMPLATE.format(product_ids)
        filepath = os.path.join(RESULTS_DIR, filename)

        pd.DataFrame(reviews).to_csv(filepath, index=False)
        print(f"Данные сохранены в {filepath}")

