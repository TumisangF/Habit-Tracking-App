from database import HabitDatabase

class HabitAnalytics:
    """
    Analytics offers the ability to analyze habits depending on how frequently they occur.
    """
    def __init__(self, database):
        self.habit_database = database

    def analyze_habits(self):
        """
        Examines habits and displays the longest streak for each habit.

        After the user enters a frequency (daily/weekly), it will display the highest streak from all habits of that frequency.
        Then, it will list the habits and their respective streaks for that frequency.

        Returns:
            None
        """
        print("Enter the frequency to analyze (daily/weekly):")
        frequency = input().strip().lower()

        habits = self.habit_database.get_habits_by_frequency(frequency)

        if not habits:
            print(f"No {frequency} habits found.")
            return

        print(f"\n{frequency.capitalize()} Habit Analysis:")
        highest_streak_habit = [] # To handle the edge case of having multiple habits with the highest streak. Habits are going to be stored in a list
        highest_streak = 0
        shortest_streak_habit = None
        shortest_streak = float('inf')
        
        for habit in habits:
            name, streak = habit
            print(f"{name} - Highest Streak: {streak} {'days' if frequency == 'daily' else 'weeks'}")
            if streak > highest_streak:
                highest_streak = streak
                highest_streak_habit = [name]
            elif streak == highest_streak:
                highest_streak_habit.append(name)
            if streak < shortest_streak:
                shortest_streak = streak
                shortest_streak_habit = [name]
            elif streak == shortest_streak:
                shortest_streak_habit.append(name)

        print("\nLongest running streak:")
        if highest_streak_habit:
            habit_list = ", ".join(highest_streak_habit)
            print(f"The highest streak from {frequency} habits is {habit_list} - {highest_streak} {'days' if frequency == 'daily' else 'weeks'}.")
        else:
            print(f"No habits found for {frequency} frequency.")
        
        print("\nHabit you struggled with the most:")
        if shortest_streak_habit:
            habit_list = ", ".join(shortest_streak_habit)
            print(f"Habit with the shortest streak from {frequency} habits is {habit_list} - {shortest_streak} {'days' if frequency == 'daily' else 'weeks'}.")
        print("\nEnter the habit name for further analysis (type 'exit' to go back):")
        habit_name = input().strip().capitalize()

        if habit_name.lower() == 'exit':
            return

        habit = self.habit_database.get_habit(habit_name)

        if habit:
            _, count, _, _ = habit
            print(f"\nThe habit has been completed {count} times.")
        else:
            print(f"Habit '{habit_name}' not found.")