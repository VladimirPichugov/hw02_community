import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    date = datetime.datetime.today()
    year = int(date.strftime('%Y'))
    return {
        'year': year
    }