import pytest

from scr.model.employees import Employee
from scr.parsers.parsers import ParserCsv


@pytest.fixture
def csv_text():
    return (
        'department,id,email,name,hours_worked,hourly_rate\n'
        'HR,101,grace@example.com,Grace Lee,160,45\n'
        'Marketing,102,henry@example.com,Henry Martin,150,35'
    )


def test_parser_initialization(csv_text):
    assert ParserCsv(csv_text).lines == [
        'department,id,email,name,hours_worked,hourly_rate',
        'HR,101,grace@example.com,Grace Lee,160,45',
        'Marketing,102,henry@example.com,Henry Martin,150,35'
    ]
    assert ParserCsv(csv_text).headers == [
        'department', 'id', 'email', 'name', 'hours_worked', 'hourly_rate'
    ]


@pytest.mark.parametrize(
    "csv_text, expected_headers",
    [
        (
            'dept,emp_id,mail,fullname,hours,rate\n1,Marketing,Alice,'
            'alice@example.com,160,50',
            ['department', 'id', 'email', 'name', 'hours_worked',
             'hourly_rate'],
        ),
        (
            'division,employee_id,e-mail,full_name,worked_hours,salary\n'
            '1,Marketing,Alice,alice@example.com,160,50',
            ['department', 'id', 'email', 'name', 'hours_worked',
             'hourly_rate'],
        ),
        (
            'unknown,id,name\n1,Marketing,Alice,alice@example.com,160,50',
            ['unknown', 'id', 'name'],
        ),
        (
            '',
            [],
        ),
    ]
)
def test_normalization_of_headers_parametrized(csv_text, expected_headers):
    parser = ParserCsv(csv_text)
    parser._normalization_of_headers()
    assert parser.headers == expected_headers


def test_parser_data(csv_text):
    data = ParserCsv(csv_text)
    assert data.parser_data() == [
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
    ]


def test_parser_data_not_data():
    data = ParserCsv('')
    assert data.parser_data() == []
