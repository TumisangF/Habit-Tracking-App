import pytest
from habitTracker import HabitTracker
from database import HabitDatabase
from analytics import HabitAnalytics


@pytest.fixture
def habit_db():
    db = HabitDatabase()
    yield db
    db.conn.close()  # Close the connection after each test.

@pytest.fixture
def habit_tracker():
    tracker = HabitTracker()
    yield tracker
    #tracker.conn.close()  # Close the connection after each test.

@pytest.fixture
def habit_analytics():
    analytics = HabitAnalytics()
    yield analytics
    #analytics.conn.close()  # Close the connection after each test.

def test_create_habit_database(habit_db):
    # Test creating a new habit database
    assert habit_db is not None

# Test case for checking if predefined habits are added to the 'habits' table.
def test_create_predefined_habits(habit_db):
    habit_db.cursor.execute("SELECT COUNT(*) FROM habits;")
    count = habit_db.cursor.fetchone()[0]
    assert count == 5  # Number of predefined habits in the create_predefined_habits method.

def test_add_habit(habit_db):
    # Test adding a new habit
    habit_db.add_habit("testHabit1", "daily")
    habit = habit_db.get_habit("testHabit1")
    assert habit is not None
    assert habit[0] == "daily"

def test_delete_habit(habit_db):
    # Test deleting an existing habit in the databse
    habit_db.add_habit("testHabit2", "daily")
    habit_db.delete_habit("testHabit2")
    habit = habit_db.get_habit("testHabit2")
    assert habit is None

def test_get_habit(habit_db):
    # Test getting an existing habit
    habit_db.add_habit("testHabit3", "daily")
    habit = habit_db.get_habit("testHabit3")
    assert habit is not None
    assert habit[0] == "daily"

def test_track_daily_habit(habit_db):
    track = HabitTracker(habit_db)
    track.habit_database.add_habit("testHabit4", "daily")
    track.track_habit("testHabit4")

    habit = habit_db.get_habit("testHabit4")
    _, count, current_streak, highest_streak = habit
    assert count == 1
    assert current_streak == 1
    assert highest_streak == 0

def test_track_weekly_habit(habit_db):
    track = HabitTracker(habit_db)
    track.habit_database.add_habit("testHabit5", "weekly")
    track.track_habit("testHabit5")

    habit = habit_db.get_habit("testHabit5")
    _, count, current_streak, highest_streak = habit
    assert count == 1
    assert current_streak == 1
    assert highest_streak == 0

def test_higher_streak_daily(habit_db):
    #streak = HabitDatabase()
    dailyTrackingData = {
                "Eat Vegies": ["2023-06-25", "2023-06-26", "2023-06-27","2023-06-29"]}
    for habit, dates in dailyTrackingData.items():
        dailyHigherStreak = habit_db.calculate_daily_highest_streak(dates)
        dailyTotalCount = len(dates)
        assert dailyHigherStreak == 3
        assert dailyTotalCount == 4

def test_higher_streak_weekly(habit_db):
    #streak = HabitDatabase()
    weeklyTrackingData = {
                "Laundry": ["2023-06-14", "2023-06-21"]}
    for habit, dates in weeklyTrackingData.items():
        weeklyHigherStreak = habit_db.calculate_weekly_highest_streak(dates)
        weeklyTotalCount = len(dates)
        assert weeklyHigherStreak == 2
        assert weeklyTotalCount == 2

    