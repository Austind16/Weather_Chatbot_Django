from datetime import datetime, timedelta


class DateResolver:

    WEEKDAYS = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    @staticmethod
    def resolve(date_text):

        if not date_text:
            return None

        date_text = date_text.lower().strip()

        today = datetime.now().date()

        # Relative dates
        if date_text == "today":
            return today

        if date_text == "tomorrow":
            return today + timedelta(days=1)

        if date_text == "yesterday":
            return today - timedelta(days=1)

        # Weekdays
        if date_text in DateResolver.WEEKDAYS:

            target_weekday = DateResolver.WEEKDAYS[date_text]
            current_weekday = today.weekday()

            days_ahead = (target_weekday - current_weekday) % 7

            # If today is the requested weekday,
            # use the next occurrence.
            if days_ahead == 0:
                days_ahead = 7

            return today + timedelta(days=days_ahead)

        return None