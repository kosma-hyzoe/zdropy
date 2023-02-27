from models import ClassInfo

valid_class_info = ClassInfo(
    name='Pilates',
    time='09:30',
    date='2023-02-28',
    club="Zdrofit Bemowo"
)

invalid_class_info = ClassInfo(
    name='foobar',
    time='10:00',
    date='2023-02-29',
    club="Zdrofit Bemowo"
)
