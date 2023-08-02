from datetime import datetime, timedelta
import sqlite3

# This module offers a class for gaining access to a database.

class HabitDatabase:
    """ 
    HabitDatabase gives users access to a SQLite database for managing habits and the data used to track them.

    habits can be added , removed and retrieved using the HabitDatabase class.
    It also offers ways to establish predefined routines and keep track of their streaks.

    Attributes:
            conn (sqlite3.Connection): A SQLite database connection object, 
            cursor object (sqlite3.Cursor):is used for interaction with the database.
    """

    def __init__(self):
        self.conn = sqlite3.connect('habits.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.create_predefined_habits()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS habits
                            (name TEXT PRIMARY KEY, frequency TEXT, count INTEGER, current_streak INTEGER, highest_streak INTEGER)''')

        self.conn.commit()

    def calculate_daily_highest_streak(self, dates):
        """Calculate the highest streak from a list of daily dates.

        Args:
            dates (list): A list of date strings in the format "YYYY-MM-DD".

        Returns:
            int: The highest streak from the list of dates.
        """
        sorted_dates = sorted(dates)
        current_streak = 1
        highest_streak = 1

        for i in range(1, len(sorted_dates)):
            current_date = datetime.strptime(sorted_dates[i], "%Y-%m-%d")
            prev_date = datetime.strptime(sorted_dates[i - 1], "%Y-%m-%d")
            delta = (current_date - prev_date).days

            if delta == 1:
                current_streak += 1
                if current_streak > highest_streak:
                    highest_streak = current_streak
            else:
                current_streak = 1

        return highest_streak

    def calculate_weekly_highest_streak(self, dates):
        """Calculate the highest streak from a list of weekly dates.

        Args:
            dates (list): A list of date strings in the format "YYYY-MM-DD".

        Returns:
            int: The highest streak from the list of dates.
        """
        sorted_dates = sorted(dates)
        current_streak = 1
        highest_streak = 1
    

        for i in range(1, len(sorted_dates)):
            current_date = datetime.strptime(sorted_dates[i], "%Y-%m-%d")
            prev_date = datetime.strptime(sorted_dates[i - 1], "%Y-%m-%d")
            delta = (current_date - prev_date).days

            if delta <= 7:
                current_streak += 1
                if current_streak > highest_streak:
                    highest_streak = current_streak
            else:
                current_streak = 1

        return highest_streak

    def create_predefined_habits(self):
        """
        Creates predefined habits in the habits table.

        The habits are:
            - Drink 5 glasses of water
            - Exercise
            - Read a book
            - Meditate
            - Take a 30-minute walk
        """
        
        self.cursor.execute('SELECT COUNT(*) FROM habits')
        result = self.cursor.fetchone()
        if result[0] == 0:  # Check if the habits table is empty
            predefined_habits = [
                ("Drink 5 glasses of water", "daily"),
                ("Exercise", "weekly"),
                ("Read a book", "daily"),
                ("Meditate", "daily"),
                ("Take a 30-minute walk", "weekly"),
            ]
            for habit, frequency in predefined_habits:
                self.cursor.execute('INSERT INTO habits (name, frequency, count, current_streak, highest_streak) VALUES (?, ?, 0, 0, 0)', (habit, frequency))

            dailyTrackingData = {
                "Drink 5 glasses of water": ["2023-06-01", "2023-06-02", "2023-06-03", "2023-06-04", "2023-06-06", "2023-06-08", "2023-06-09", "2023-06-15", "2023-06-22"],
                "Read a book": ["2023-06-01", "2023-06-02", "2023-06-03", "2023-06-04", "2023-06-05", "2023-06-06", "2023-06-10", "2023-06-11", "2023-06-12", "2023-06-15", "2023-06-16", "2023-06-17", "2023-06-18", "2023-06-22", "2023-06-23", "2023-06-24", "2023-06-25", "2023-06-26"],
                "Meditate": ["2023-06-01", "2023-06-02", "2023-06-03", "2023-06-04", "2023-06-05", "2023-06-06", "2023-06-10", "2023-06-11", "2023-06-18", "2023-06-28"],
            }
            weeklyTrackingData = {
                "Exercise": ["2023-06-06", "2023-06-13", "2023-06-20"],
                "Take a 30-minute walk": ["2023-06-06", "2023-06-12"],
            }
            # Extracting highest streak and total count from daily tracking data for the month of June 2023.
            for habit, dates in dailyTrackingData.items():
                daily_highest_streak = self.calculate_daily_highest_streak(dates)
                daily_total_count = len(dates)

                self.cursor.execute('UPDATE habits SET highest_streak = ? WHERE name = ?', (daily_highest_streak, habit))
                self.cursor.execute('UPDATE habits SET count = ? WHERE name = ?', (daily_total_count, habit))

            # Extracting highest streak and total count from weekly tracking data for the month of June.
            for habit, dates in weeklyTrackingData.items():
                weekly_highest_streak = self.calculate_weekly_highest_streak(dates)
                weekly_total_count = len(dates)

                self.cursor.execute('UPDATE habits SET highest_streak = ? WHERE name = ?', (weekly_highest_streak, habit))
                self.cursor.execute('UPDATE habits SET count = ? WHERE name = ?', (weekly_total_count, habit))

        self.conn.commit()


    def add_habit(self, name, frequency):
        """
        Adds a new habit with the given name and frequency to the habits table.

        Args: name (str): 
            The habit's name that has to be added.
        Frequency (str): 
            the consistency (daily or weekly) of the habit.

        Returns: 
            None
        """
        self.cursor.execute('INSERT INTO habits (name, frequency, count, current_streak, highest_streak) VALUES (?, ?, 0, 0, 0)', (name, frequency))
        self.conn.commit()
        print(f'Habit "{name}" added successfully.')

    def delete_habit(self, name):
        """
        Deletes a habit with the given name from the habits table.

        Args: name (str): 
            The habit's name that has to be deleted.

        Returns: 
            None
        """
        self.cursor.execute('SELECT COUNT(*) FROM habits WHERE name = ?', (name,))
        result = self.cursor.fetchone()
        if result[0] > 0:  # Check if the habit exists in the database
            self.cursor.execute('DELETE FROM habits WHERE name = ?', (name,))
            self.conn.commit()
            print(f'Habit "{name}" deleted successfully.')
        else:
            print(f'Habit "{name}" does not exist.')

    def get_habit(self, name):
        self.cursor.execute('SELECT frequency, count, current_streak, highest_streak FROM habits WHERE name = ?', (name,))
        return self.cursor.fetchone()

    def update_habit(self, name, frequency, count, current_streak, highest_streak):
        self.cursor.execute('UPDATE habits SET frequency = ?, count = ?, current_streak = ?, highest_streak = ? WHERE name = ?', (frequency, count, current_streak, highest_streak, name))
        self.conn.commit()
    
    def list_habits(self):
        self.cursor.execute('SELECT name, frequency FROM habits')
        habits = self.cursor.fetchall()
        if not habits:
            print('No habits found.')
        else:
            print('Habits:')
            for habit in habits:
                name, frequency = habit
                print(f'{name} ({frequency})')
    
    def get_all_habits(self, frequency=None):
        if frequency:
            self.cursor.execute('SELECT name, highest_streak FROM habits WHERE frequency = ?', (frequency,))
        else:
            self.cursor.execute('SELECT name, highest_streak FROM habits')
        habits = self.cursor.fetchall()
        return habits

    def get_habits_by_frequency(self, frequency):
        return self.get_all_habits(frequency)
