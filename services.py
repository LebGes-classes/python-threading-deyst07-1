"""Классы для генерации отчётов."""


import pandas as pd
from const import CALIBRATION_THRESHOLD_DAYS, TOP_CLINICS_LIMIT


class WarrantyService:
    """Сервис для фильтрации устройств по гарантии."""

    def __init__(self, df, warranty_column='warranty_until'):
        """
        Инициализирует сервис.

        Args:
            df: DataFrame с данными.
            warranty_column: Название колонки с датой гарантии.
        """
        
        self.df = df.copy()
        self.warranty_column = warranty_column
    
    def filter(self):
        """
        Фильтрует устройства на гарантии.

        Returns:
            DataFrame с устройствами на гарантии.
        """
        
        today = pd.Timestamp.today()
        self.df['is_under_warranty'] = (
            self.df[self.warranty_column] > today
        )
        
        return self.df[self.df['is_under_warranty']].copy()

 
class ClinicService:
    """Сервис для анализа клиник."""

    def __init__(self, df, limit=TOP_CLINICS_LIMIT):
        """
        Инициализирует сервис.

        Args:
            df: DataFrame с данными.
            limit: Количество клиник в топе.
        """
        
        self.df = df.copy()
        self.limit = limit

    def get_top_problems(self):
        """
        Находит клиники с наибольшим количеством проблем.

        Returns:
            DataFrame с топ-клиниками.
        """
        
        self.df['total_issues'] = (
            self.df['issues_reported_12mo'] + 
            self.df['failure_count_12mo']
        )

        result = self.df.groupby('clinic_name').agg(
        total_issues=('total_issues', 'sum'),
        devices_count=('device_id', 'count'),
        total_failures=('failure_count_12mo', 'sum'),
        )

        result = result.sort_values(
            'total_issues', 
            ascending=False
        ).head(self.limit)

        return result.reset_index()
    

class CalibrationService:
    """Сервис для отчёта по калибровке."""

    def __init__(self, df, threshold_days=CALIBRATION_THRESHOLD_DAYS):
        """
        Инициализирует сервис.

        Args:
            df: DataFrame с данными.
            threshold_days: Порог дней для калибровки.
        """
        
        self.df = df.copy()
        self.threshold_days = threshold_days

    def generate_report(self):
        """
        Генерирует отчёт по калибровке.

        Returns:
            DataFrame с отчётом.
        """
        
        today = pd.Timestamp.today()

        self.df['days_since_calibration'] = (
            today - self.df['last_calibration_date']
        ).dt.days.fillna(-1).astype(int)

        self.df['calibration_needed'] = (
            (self.df['days_since_calibration'] > self.threshold_days) |
            (self.df['last_calibration_date'].isna())
        )

        invalid_mask = (
            self.df['last_calibration_date'] < self.df['install_date']
        )
        self.df.loc[invalid_mask, 'calibration_needed'] = True

        columns = [
            'device_id', 'clinic_name', 'model',
            'last_calibration_date', 'days_since_calibration',
            'calibration_needed',
        ]
        columns = [col for col in columns if col in self.df.columns]

        result = self.df[columns].sort_values(
            'days_since_calibration', 
            ascending=False
        )
        
        return result
    

class AggregationService:
    """Сервис для сводных таблиц."""

    def __init__(self, df):
        """
        Инициализирует сервис.

        Args:
            df: DataFrame с данными.
        """
        
        self.df = df.copy()

    def create_pivot(self):
        """Создаёт сводную таблицу."""
        
        self.df['total_issues'] = (
            self.df['issues_reported_12mo'] + 
            self.df['failure_count_12mo']
        )

        result = self.df.groupby(['clinic_name', 'model']).agg(
            devices_count=('device_id', 'count'),
            avg_uptime_pct=('uptime_pct', 'mean'),
            total_issues=('total_issues', 'sum'),
            total_failures=('failure_count_12mo', 'sum'),
        ).round(2)

        result = result.sort_values('total_issues', ascending=False)
        
        return result.reset_index()
    

class ReportExporter:
    """Сервис для экспорта отчётов в Excel."""

    def __init__(self, output_path):
        """
        Инициализирует экспортер.

        Args:
            output_path: Путь для сохранения файла.
        """
        
        self.output_path = output_path

    def export(self, reports_dict):
        """
        Сохраняет отчёты в Excel.

        Args:
            reports_dict: Словарь {имя_листа: DataFrame}.
        """
       
        with pd.ExcelWriter(self.output_path) as writer:
            for name, frame in reports_dict.items():
                frame.to_excel(writer, sheet_name=name, index=False)
