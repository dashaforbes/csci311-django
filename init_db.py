# run as python manage.py shell < init_db.py
from charts.models import Version, Component, People

versions = [
    '3.4',
    '3.3',
    '3.2',
    '3.1',
    '3.0',
    '2.7',
    '2.6',
    '2.5',
    '2.4',
    '2.3',
    '2.2',
    '2.0',
    '1.5',
    '1.4',
    '1.3',
    '1.2',
    '1.1',
    '1.0',
]

components = [
    '2to3 (2.x to 3.0 conversion tool)',
    'Benchmarks',
    'Build',
    'ctypes',
    'Demos and Tools',
    'Devguide',
    'Distutils',
    'Distutils2',
    'Documentation',
    'email',
    'Extension Modules',
    'IDLE',
    'Installation',
    'Interpreter Core',
    'IO',
    'Library (Lib)',
    'Macintosh',
    'Regular Expressions',
    'Tests',
    'Tkinter',
    'Unicode',
    'Windows',
    'XML',
]

people = [
    'Test',
    'John',
    'Joe',
    'Jessie',
    'Martha',
    'Samantha',
    'Peter',
    'Pablo',
    'Timothy',
    'Cameron',
    'Nancy',
    'Nichael',
    'leet_hacker_77',
    'Richard',
    'Adrian',
    'Liam',
    'Lisa',
    'William',
    'Diana',
    'Paul',
]

for version in versions:
    v = Version(version=version)
    v.save()

for component_name in components:
    c = Component(name=component_name)
    c.save()

for person in people:
    p = People(username=person)
    p.save()

