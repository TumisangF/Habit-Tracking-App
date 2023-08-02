import datetime

#HabitTracker module is in charge of keeping track of habits and updating the database of habits with their current status.
class HabitTracker:
    
    def __init__(self, habit_database):
        """
        Initializes the HabitTracker with the given HabitDatabase.

        Args:
            habit_database (HabitDatabase): An instance of the HabitDatabase class to connect with the habits database.
        """
        self.habit_database = habit_database

    def track_habit(self, name: str):
        """
        Track the progress of a habit and update its status in the habit database by incrementing the number of times a habit has been completed.

        Args:
            name (str): The name of the habit to track.
        """
        habit = self.habit_database.get_habit(name)
        if habit:
            frequency, count, current_streak, highest_streak = habit
            today = datetime.date.today()

            if frequency == 'daily':
                # Check if last tracked day is the previous day.
                if today == (today - datetime.timedelta(days=1)):
                    current_streak += 1
                    if current_streak > highest_streak:
                        highest_streak = current_streak
                else:
                    # Check if there was a break in the habit
                    current_streak = 1 if today != (today - datetime.timedelta(days=1)) else current_streak
                    
            elif frequency == 'weekly':
                # Assuming weeks start on Monday (0) and end on Sunday (6)
                last_sunday = today - datetime.timedelta(days=today.weekday() + 1)
                
                # Check if last tracked Sunday is a previous week.
                if last_sunday == (today - datetime.timedelta(days=7)):  
                    current_streak += 1
                    if current_streak > highest_streak:
                        highest_streak = current_streak
                else:
                    # Check if there was a break in the habit
                    current_streak = 1 if last_sunday != (today - datetime.timedelta(days=7)) else current_streak
            
            # Keep track of the number of times a habit has been completed.
            count += 1

            self.habit_database.update_habit(name, frequency, count, current_streak, highest_streak)
            print(f'Habit "{name}" tracked successfully.')
        else:
            print(f'Habit "{name}" not found.')