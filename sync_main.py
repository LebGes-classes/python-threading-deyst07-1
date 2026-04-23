import time

from models import DeviceData
from services import (
    WarrantyService,
    ClinicService,
    CalibrationService,
    AggregationService,
    ReportExporter,
)


def process_file(input_file, output_file):

    print(f"Начата обработка {input_file}")

    data = DeviceData(input_file)

    data.load()
    data.clean()

    df = data.get_dataframe()

    warranty = WarrantyService(df).filter()
    clinics = ClinicService(df).get_top_problems()
    calibration = CalibrationService(df).generate_report()
    pivot = AggregationService(df).create_pivot()

    exporter = ReportExporter(output_file)

    exporter.export(
        {
            "warranty": warranty,
            "clinics": clinics,
            "calibration": calibration,
            "pivot": pivot,
        }
    )

    print(f"{input_file} завершён")



def main():

    start = time.time()

    for i in range(1, 11):

        process_file(
            f"medical_diagnostic_devices_{i}.xlsx",
            f"report_{i}.xlsx",
        )

    print("Sync время:", time.time() - start)


if __name__ == "__main__":
    main()
