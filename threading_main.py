import threading
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

    warranty = None
    clinics = None
    calibration = None
    pivot = None


    def warranty_worker():
        nonlocal warranty
        warranty = WarrantyService(df).filter()


    def clinics_worker():
        nonlocal clinics
        clinics = ClinicService(df).get_top_problems()


    def calibration_worker():
        nonlocal calibration
        calibration = CalibrationService(df).generate_report()


    def pivot_worker():
        nonlocal pivot
        pivot = AggregationService(df).create_pivot()


    t1 = threading.Thread(target=warranty_worker)
    t2 = threading.Thread(target=clinics_worker)
    t3 = threading.Thread(target=calibration_worker)
    t4 = threading.Thread(target=pivot_worker)


    t1.start()
    t2.start()
    t3.start()
    t4.start()


    t1.join()
    t2.join()
    t3.join()
    t4.join()


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

    threads = []

    for i in range(1, 11):

        t = threading.Thread(
            target=process_file,
            args=(
                f"medical_diagnostic_devices_{i}.xlsx",
                f"report_{i}.xlsx",
            )
        )

        threads.append(t)
        t.start()


    for t in threads:
        t.join()


    print("Мультипоток время:", time.time() - start)


if __name__ == "__main__":
    main()
