class YearConverter:
    regex = '-?[0-9]{1,4}'

    def to_python(self, value):
        year = int(value)
        if year < 1000 or year > 2026:
            raise Http404(f"Год {year} вне допустимого диапазона")
        return year

    def to_url(self, value):
        return str(value)