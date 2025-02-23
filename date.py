from datetime import datetime


def is_less_than_25days(term_text):
    # Get the current date
    today = datetime.today()

    # Convert the string into a date, adding the current year
    term_date_str = f"{term_text}.{today.year}"

    try:
        term_date = datetime.strptime(term_date_str, "%d.%m.%Y")
    except ValueError:
        print("Error: Invalid date format")
        return None

    # If the date has already passed this year, use the next year
    if term_date < today:
        term_date = term_date.replace(year=today.year + 1)

    # Check the difference in days
    return (term_date - today).days <= 25
