from abc import ABC
import json
from typing import List

from scr.model.departments import Department
from scr.model.employees import Employee


class Report(ABC):
    def __init__(self, data: List[Employee]):
        self.data = data

    def _group_by_departments(self) -> List[Department]:
        num_dep = {}
        departments = []
        for emp in self.data:
            if emp.department not in [dep.title for dep in departments]:
                departments.append(Department(emp.department))
                departments[-1].add_employee(emp)
                num_dep[emp.department] = len(departments) - 1
            elif emp.department in [dep.title for dep in departments]:
                departments[num_dep[emp.department]].add_employee(emp)
        return departments


class Payout(Report):
    def payout_to_terminal(self) -> None:
        # Группировка по департаментам
        departments = self._group_by_departments()

        # Вывод результатов в терминал
        print(
            '                        name                         '
            'hours     rate     payout')
        for department in departments:
            print(f'{department}')

            for emp in department.list_emp:
                name = emp.name.ljust(30)
                hours = str(emp.hours_worked).rjust(6)
                rate = str(emp.hourly_rate).rjust(6)
                payout = f'${emp.payout}'.rjust(10)
                print(
                    f'-------------------- {name}{hours}    {rate}    '
                    f'{payout}')

            print(f'{"":54}{str(department.total_hours)}                   '
                  f'${str(department.total_payout)}')

    def payout_to_json(self, output_file: str = 'output.json') -> None:
        # Группировка данных по департаментам для JSON
        departments = self._group_by_departments()

        # Формируем структурированный словарь для JSON
        result = {}
        for department in departments:
            result[department.__repr__()] = {
                'employees': [
                    {
                        'name': emp.name,
                        'hours_worked': emp.hours_worked,
                        'hourly_rate': emp.hourly_rate,
                        'payout': emp.payout
                    }
                    for emp in department.list_emp
                ],
                'total_hours': department.total_hours,
                'total_payout': department.total_payout
            }

        # Сохраняем в JSON-файл
        try:
            with open(f'{output_file}', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print(f'Данные успешно сохранены в файл "{output_file}"')
        except Exception as e:
            print(f'Ошибка при сохранении в файл "{output_file}": {e}')
