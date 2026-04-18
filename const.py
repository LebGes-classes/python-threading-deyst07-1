"""Константы."""


INPUT_FILE = 'medical_diagnostic_devices_10000.xlsx'
OUTPUT_FILE = 'medical_report.xlsx'

DATE_COLUMNS = [
    'install_date',
    'warranty_until',
    'last_calibration_date',
    'last_service_date',
]

NUMERIC_COLUMNS = [
    'issues_reported_12mo',
    'failure_count_12mo',
    'uptime_pct',
]

STATUS_MAPPING = {
    'ok': 'operational',
    'op': 'operational',
    'working': 'operational',
    'operational': 'operational',
    'planned': 'planned_installation',
    'to_install': 'planned_installation',
    'scheduled_install': 'planned_installation',
    'planned_installation': 'planned_installation',
    'maintenance': 'maintenance_scheduled',
    'service_scheduled': 'maintenance_scheduled',
    'maint_sched': 'maintenance_scheduled',
    'maintenance_scheduled': 'maintenance_scheduled',
    'needs_repair': 'faulty',
    'broken': 'faulty',
    'error': 'faulty',
    'faulty': 'faulty',
}

CALIBRATION_THRESHOLD_DAYS = 365
TOP_CLINICS_LIMIT = 100
