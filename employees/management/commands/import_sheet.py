# employees/management/commands/import_sheet.py

import pandas as pd
from tqdm import tqdm
from django.core.management.base import BaseCommand
from employees.models import File, PaymentType

class Command(BaseCommand):
    help = "Import Files and PaymentTypes from an Excel sheet"

    def add_arguments(self, parser):
        parser.add_argument('path',  type=str, help="Excel file path")
        parser.add_argument('sheet', type=str, help="Sheet name in the workbook")

    def handle(self, *args, **options):
        path       = options['path']
        sheet_name = options['sheet']

        # Read the sheet
        df = pd.read_excel(path, sheet_name=sheet_name)

        for _, row in tqdm(df.iterrows(), total=len(df), desc="Importing"):
            file_num     = int(row['FILE'])
            service_type = str(row['TRX']).strip()
            insurance    = str(row['COMP']).strip().capitalize()
            patient_name = str(row['NAME']).strip()

            # Lookup by number only; then update name if needed
            file_obj, created = File.objects.get_or_create(number=file_num)
            if created or file_obj.patient_name != patient_name:
                file_obj.patient_name = patient_name
                file_obj.save()

            # No duplicate per (file, service_type, insurance)
            PaymentType.objects.get_or_create(
                file=file_obj,
                service_type=service_type,
                insurance=insurance,
                defaults={'num_of_session': 10}
            )

        self.stdout.write(self.style.SUCCESS("Files and PaymentTypes imported successfully."))
