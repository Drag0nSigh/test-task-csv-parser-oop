from scr.constance.constance import HEADER
from scr.model.employees import Employee


class ParserCsv(object):
    def __init__(self, csv_text: str):
        self.lines = csv_text.strip().split('\n')
        if not self.lines or not self.lines[0].strip():
            self.headers = []
        else:
            self.headers = self.lines[0].split(',')

    def _normalization_of_headers(self):
        for i, head in enumerate(self.headers):
            for key, value in HEADER.items():
                if head in value:
                    self.headers[i] = key

    def parser_data(self):
        self._normalization_of_headers()
        data = []
        for line in self.lines[1:]:
            values = line.split(',')
            row = {}
            for i, header in enumerate(self.headers):
                if header in ['id', 'hours_worked', 'hourly_rate']:
                    row[header] = int(values[i])
                else:
                    row[header] = values[i]
            emp = Employee(
                id=row.get('id'),
                name=row.get('name', ''),
                department=row.get('department'),
                hours_worked=row.get('hours_worked', 0),
                hourly_rate=row.get('hourly_rate', 0),
                email=row.get('email', 0),
                payout=row.get('hours_worked', 0) * row.get('hourly_rate', 0),
            )
            data.append(emp)
        return data
