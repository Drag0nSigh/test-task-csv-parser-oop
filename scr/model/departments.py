from scr.model.employees import Employee


class Department:
    def __init__(self, title: str):
        self.title = title
        self.total_hours = 0
        self.count = 0
        self.total_payout = 0
        self.list_emp = []

    def add_employee(self, emp: Employee):
        self.total_hours += emp.hours_worked
        self.total_payout += emp.hours_worked * emp.hourly_rate
        self.count += 1
        self.list_emp.append(emp)

    def __repr__(self):
        return f'{self.title}'
