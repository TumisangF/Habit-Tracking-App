from database import HabitDatabase
from habitTracker import HabitTracker
from analytics import HabitAnalytics

"""
This module is responsible for handling the user interface.
"""

def main():
    """ 
    The primary purpose of the habit tracking programme.

    The HabitDatabase, HabitTracker, and HabitAnalytics objects are initialised using this function.
    The user is given a command-line interface for managing, tracking, and analysing habit data.
    The user can create, and list their habits, monitor their progrss by analysing habit streaks.

    Returns:

        None

    """
    habit_database = HabitDatabase()
    habit_database.create_predefined_habits()

    habit_tracker = HabitTracker(habit_database)
    habit_analytics = HabitAnalytics(habit_database)

    while True:
        print("\nWelcome to the Habit Tracking Application\n")
        print("Enter a command:")
        print("1. Add a habit")
        print("2. Delete a habit")
        print("3. Track a habit")
        print("4. List habits")
        print("5. Analyze habits")
        print("6. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == '1':
            name = input("Enter habit name: ").strip().capitalize()
            frequency = input("Enter habit frequency (daily/weekly): ").strip().lower()
            habit_database.add_habit(name, frequency)

        elif choice == '2':
            name = input("Enter habit name to delete: ").strip().capitalize()
            habit_database.delete_habit(name)

        elif choice == '3':
            name = input("Enter habit name to track: ").strip().capitalize()
            habit_tracker.track_habit(name)

        elif choice == '4':
            habit_database.list_habits()

        elif choice == '5':
            habit_analytics.analyze_habits()

        elif choice == '6':
            print("Exiting the application.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()