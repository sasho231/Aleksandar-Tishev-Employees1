import datetime


class Project:
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end


class Employee:
    def __init__(self, id):
        self.id = id
        self.projects = {}
        self.colleagues = {}

    def addProject(self, project):
        self.projects[project.id] = project

    def addColleague(self, empl, timeTogether):
        self.colleagues[empl.id] = timeTogether


employees = {}


def get_time_working_together(emp1, emp2):
    time_together_in_days = 0;
    for key in emp1.projects:
        if key in emp2.projects:
            if emp1.projects[key].start < emp2.projects[key].end and emp1.projects[key].end > emp2.projects[key].start:
                delta = min(emp1.projects[key].end, emp2.projects[key].end) - max(emp1.projects[key].start,
                                                                                  emp2.projects[key].start)
                time_together_in_days += delta.days;
    return time_together_in_days


with open("employees.csv", "r") as file:
    for line in file:
        args = line.strip().split(", ")
        start = datetime.datetime.strptime(args[2], '%Y-%m-%d')
        end = datetime.datetime.today() if args[3] == 'NULL' else datetime.datetime.strptime(args[3], '%Y-%m-%d')
        prj = Project(args[1], start, end)

        if (args[0] not in employees):
            empl = Employee(args[0])
            empl.addProject(prj)
            employees[args[0]] = empl
        else:
            employees[args[0]].addProject(prj)

for key in employees:
    for key1 in employees:
        if (key != key1):
            total = get_time_working_together(employees[key], employees[key1])
            if (total != 0):
                employees[key].addColleague(employees[key1], total)

max_days_together = -1;
empl1 = ''
empl2 = ''

for emplKey in employees:
    for collKey in employees[emplKey].colleagues:
        if (employees[emplKey].colleagues[collKey] > max_days_together):
            max_days_together = employees[emplKey].colleagues[collKey]
            empl1 = employees[emplKey]
            empl2 = employees[collKey]

if max_days_together > -1:
    print('The employees working together the longest are {} and {} with total of {} days working together'
          .format(empl1.id, empl2.id, max_days_together))
else:
    print("No emplyees have ever worked together")