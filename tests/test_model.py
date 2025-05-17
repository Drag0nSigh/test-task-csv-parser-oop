import json
from typing import List

import pytest

from scr.model.departments import Department
from scr.model.employees import Employee
from scr.model.report import Payout, Report


@pytest.fixture
def sample_employee():
    return Employee(
        id=1,
        name='Alice Johnson',
        department='Marketing',
        hours_worked=160,
        hourly_rate=50,
        email='alice@example.com',
        payout=8000,
    )


@pytest.fixture
def sample_department():
    return Department(title='Marketing')


@pytest.fixture
def sample_employees() -> List[Employee]:
    return [
        Employee(
            id=101,
            name='Grace Lee',
            department='HR',
            email='grace@example.com',
            hours_worked=160,
            hourly_rate=45,
            payout=7200,
        ),
        Employee(
            id=102,
            name='Henry Martin',
            department='Marketing',
            email='henry@example.com',
            hours_worked=150,
            hourly_rate=35,
            payout=5250,
        ),
        Employee(
            id=103,
            name='Alice Johnson',
            department='HR',
            email='alice@example.com',
            hours_worked=170,
            hourly_rate=50,
            payout=8500,
        ),
    ]


@pytest.fixture
def sample_report(sample_employees) -> Report:
    return Report(sample_employees)


@pytest.fixture
def sample_payout(sample_employees) -> Payout:
    return Payout(sample_employees)


def test_employee_initialization(sample_employee):
    assert vars(sample_employee) == {
        'id': 1,
        'name': 'Alice Johnson',
        'department': 'Marketing',
        'email': 'alice@example.com',
        'hours_worked': 160,
        'hourly_rate': 50,
        'payout': 8000,
    }


def test_employee_attributes(sample_employee):
    assert sample_employee.id == 1
    assert sample_employee.name == 'Alice Johnson'


def test_employee_types(sample_employee):
    assert isinstance(sample_employee.id, int)
    assert isinstance(sample_employee.name, str)
    assert isinstance(sample_employee.department, str)
    assert isinstance(sample_employee.email, str)
    assert isinstance(sample_employee.hours_worked, int)
    assert isinstance(sample_employee.hourly_rate, int)
    assert isinstance(sample_employee.payout, int)


def test_department_initialization(sample_department):
    assert vars(sample_department) == {
        'title': 'Marketing',
        'total_hours': 0,
        'count': 0,
        'total_payout': 0,
        'list_emp': [],
    }


def test_department_add_employee(sample_department, sample_employee):
    sample_department.add_employee(sample_employee)
    assert vars(sample_department) == {
        'count': 1,
        'list_emp': [
            Employee(
                id=1,
                name='Alice Johnson',
                department='Marketing',
                email='alice@example.com',
                hours_worked=160,
                hourly_rate=50,
                payout=8000,
            ),
        ],
        'title': 'Marketing',
        'total_hours': 160,
        'total_payout': 8000,
    }


def test_report_initialization(sample_report, sample_employees):
    assert sample_report.data == sample_employees
    assert isinstance(sample_report, Report)


def test_payout_initialization(sample_payout, sample_employees):
    assert sample_payout.data == sample_employees
    assert isinstance(sample_payout, Payout)
    assert isinstance(sample_payout, Report)


@pytest.mark.parametrize(
    'employees, expected_departments',
    [
        (
            [
                Employee(id=101, name='Grace Lee',
                         department='HR',
                         email='grace@example.com',
                         hours_worked=160,
                         hourly_rate=45,
                         payout=7200),
                Employee(id=102, name='Henry Martin',
                         department='Marketing',
                         email='henry@example.com',
                         hours_worked=150,
                         hourly_rate=35,
                         payout=5250),
            ],
            [
                {'title': 'HR',
                 'count': 1,
                 'total_hours': 160,
                 'total_payout': 7200,
                 'employee_names': ['Grace Lee']},
                {'title': 'Marketing',
                 'count': 1,
                 'total_hours': 150,
                 'total_payout': 5250,
                 'employee_names': ['Henry Martin']},
            ],
        ),
        (
            [
                Employee(id=101,
                         name='Grace Lee',
                         department='HR',
                         email='grace@example.com',
                         hours_worked=160,
                         hourly_rate=45,
                         payout=7200),
                Employee(id=103,
                         name='Alice Johnson',
                         department='HR',
                         email='alice@example.com',
                         hours_worked=170,
                         hourly_rate=50,
                         payout=8500),
            ],
            [
                {'title': 'HR',
                 'count': 2,
                 'total_hours': 330,
                 'total_payout': 15700,
                 'employee_names': ['Grace Lee', 'Alice Johnson']},
            ],
        ),
        (
            [],
            [],
        ),
    ]
)
def test_group_by_departments_parametrized(employees, expected_departments):
    payout = Payout(employees)
    departments = payout._group_by_departments()
    assert len(departments) == len(expected_departments)
    for dept, expected in zip(departments, expected_departments):
        assert dept.title == expected['title']
        assert dept.count == expected['count']
        assert dept.total_hours == expected['total_hours']
        assert dept.total_payout == expected['total_payout']
        assert ([emp.name for emp in dept.list_emp] ==
                expected['employee_names'])


def test_payout_to_terminal(sample_payout, capfd):
    sample_payout.payout_to_terminal()
    captured = capfd.readouterr()
    expected_output = (
        '                        name                         hours     rate'
        '     payout\n'
        'HR\n'
        '-------------------- Grace Lee                        160        45'
        '         $7200\n'
        '-------------------- Alice Johnson                    170        50'
        '         $8500\n'
        '                                                      330          '
        '         $15700\n'
        'Marketing\n'
        '-------------------- Henry Martin                     150        35'
        '         $5250\n'
        '                                                      150           '
        '        $5250\n'
    )
    assert captured.out == expected_output


def test_payout_to_json(sample_payout):
    output_file = 'output.json'
    sample_payout.payout_to_json(output_file=str(output_file))

    with open(output_file, 'r', encoding='utf-8') as f:
        result = json.load(f)

    expected_result = {
        'HR': {
            'employees': [
                {
                    'name': 'Grace Lee',
                    'hours_worked': 160,
                    'hourly_rate': 45,
                    'payout': 7200
                },
                {
                    'name': 'Alice Johnson',
                    'hours_worked': 170,
                    'hourly_rate': 50,
                    'payout': 8500
                }
            ],
            'total_hours': 330,
            'total_payout': 15700
        },
        'Marketing': {
            'employees': [
                {
                    'name': 'Henry Martin',
                    'hours_worked': 150,
                    'hourly_rate': 35,
                    'payout': 5250
                }
            ],
            'total_hours': 150,
            'total_payout': 5250
        }
    }
    assert result == expected_result
