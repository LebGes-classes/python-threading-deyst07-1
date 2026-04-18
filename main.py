"""Обработка данных медицинских устройств."""


from const import INPUT_FILE, OUTPUT_FILE
from models import DeviceData
from services import (
    WarrantyService,
    ClinicService,
    CalibrationService,
    AggregationService,
    ReportExporter,
)


class MedicalDevicesApp:
    """
    Главное приложение для обработки данных.
    
    Координирует работу всех сервисов.
    """

    def __init__(self, input_file, output_file):
        """
        Инициализирует приложение.

        Args:
            input_file: Путь к входному файлу.
            output_file: Путь для выходного файла.
        """
        
        self.input_file = input_file
        self.output_file = output_file
        self.data = DeviceData(input_file)
        self.exporter = ReportExporter(output_file)

    def run(self):
        """Запускает полный цикл обработки."""
        
        self._print_header()
        self._load_and_clean()
        reports = self._generate_reports()
        self._save_reports(reports)
        self._print_footer()

    def _print_header(self):
        """Выводит заголовок."""
        
        print('=' * 50)
        print('Обработка данных медицинских устройств')
        print('=' * 50)

    def _load_and_clean(self):
        """Загружает и очищает данные."""
        
        print('\n[1] Загрузка и очистка данных...')
        self.data.load().clean()
        
        print(f'    Загружено: {self.data.shape[0]} строк, '
              f'{self.data.shape[1]} колонок')
        print('    Данные очищены')

    def _generate_reports(self):
        """Генерирует все отчёты."""
        
        df = self.data.get_dataframe()

        print('\n[2] Фильтрация по гарантии...')
        warranty_df = WarrantyService(df).filter()
        print(f'    Под гарантией: {len(warranty_df)} устройств')

        print('\n[3] Анализ клиник...')
        top_clinics = ClinicService(df).get_top_problems()
        print(f'    Топ клиник: {len(top_clinics)}')

        print('\n[4] Отчёт по калибровке...')
        calibration = CalibrationService(df).generate_report()
        needed = calibration['calibration_needed'].sum()
        print(f'    Требуют калибровки: {needed}')

        print('\n[5] Сводная таблица...')
        pivot = AggregationService(df).create_pivot()
        print(f'    Строк в сводной: {len(pivot)}')

        return {
            'raw_data': df,
            'under_warranty': warranty_df,
            'top_clinics': top_clinics,
            'calibration_report': calibration,
            'pivot_summary': pivot,
        }
    
    def _save_reports(self, reports):
        """Сохраняет отчёты."""
        
        print('\n[6] Сохранение результатов...')
        self.exporter.export(reports)
        print(f'    Отчёт сохранён: {self.output_file}')

    def _print_footer(self):
        """Выводит завершение."""
        
        print('\n' + '=' * 50)
        print('Готово!')
        print('=' * 50)


def main():
    """Точка входа."""
    app = MedicalDevicesApp(INPUT_FILE, OUTPUT_FILE)
    app.run()


if __name__ == '__main__':
    main()
