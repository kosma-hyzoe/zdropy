from models import ClassInfo

valid_class_info = ClassInfo(
    name='Sztangi',
    time='10:00',
    date='2023-02-26',
    club="Zdrofit Bemowo"
)

invalid_class_info = ClassInfo(
    name='foobar',
    time='10:00',
    date='2023-02-26',
    club="Zdrofit Bemowo"
)
