"""Классы для представления и обработки данных."""


import pandas as pd
from const import STATUS_MAPPING, DATE_COLUMNS, NUMERIC_COLUMNS


class DeviceData:
    """
    Класс для хранения и очистки данных об устройствах.
    
    """

    def __init__(self, file_path):
        """
        Инициализирует объект данными из Excel.

        Args:
            file_path: Путь к Excel файлу.
        """
        
        self.file_path = file_path
        self.df = pd.DataFrame()
        self._is_cleaned = False

    def load(self):
        """Загружает данные из файла."""
        
        self.df = pd.read_excel(self.file_path)
        self._is_cleaned = False
        
        return self
    
    def clean(self):
        """
        Применяет все методы очистки данных.
        
        Returns:
            Self для цепочки вызовов.
        """
        
        if self.df is None:
            raise ValueError("Сначала загрузите данные (load())")
        
        self._clean_statuses()
        self._convert_dates()
        self._convert_numeric()
        self._is_cleaned = True
        
        return self
    
    def _clean_statuses(self, column='status'):
        """Нормализует значения статусов."""
        
        self.df[column] = self.df[column].astype(str).str.strip().str.lower().map(STATUS_MAPPING).fillna('unknown')

    def _convert_dates(self):
        """Преобразует колонки с датами в datetime."""
        
        for col in DATE_COLUMNS:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(
                    self.df[col], 
                    errors='coerce', 
                    dayfirst=True
                )

    def _convert_numeric(self):
        """Преобразует числовые колонки."""
        
        for col in NUMERIC_COLUMNS:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(
                    self.df[col], 
                    errors='coerce'
                ).fillna(0)

    @property
    def is_cleaned(self):
        """Проверяет, очищены ли данные."""
        
        return self._is_cleaned

    @property
    def shape(self):
        """Возвращает размеры DataFrame."""
        
        return self.df.shape if self.df is not None else (0, 0)

    def get_dataframe(self):
        """Возвращает DataFrame (копию для безопасности)."""
        
        return self.df.copy() if self.df is not None else None
