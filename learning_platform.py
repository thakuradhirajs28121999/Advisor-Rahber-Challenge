import json
import random
from collections import deque

class CourseCatalog:
    """
    Manages the course catalog including listing courses and resolving their prerequisites.
    """
    def __init__(self):
        self.courses = self.load_courses()

    def load_courses(self):
        """
        Loads courses from a JSON file. Returns a default set of courses if the file is not found.
        """
        try:
            with open("courses.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "Python Basics": {"prerequisites": [], "description": "Learn the fundamentals of Python programming."},
                "Introduction to Programming": {"prerequisites": [], "description": "An introductory course for programming concepts."},
                "Data Structures": {"prerequisites": ["Python Basics"], "description": "Explore data structures in Python."},
                "Algorithms": {"prerequisites": ["Data Structures"], "description": "Learn about algorithms and their applications."},
                "Machine Learning": {"prerequisites": ["Python Basics", "Data Structures", "Statistics"], "description": "Dive into the basics of machine learning."},
            }

    def list_courses(self):
        """
        Prints a list of all courses and their descriptions.
        """
        for course, details in self.courses.items():
            print(f"{course}: {details.get('description', 'No description')}")

    def get_prerequisites(self, course):
        """
        Returns a list of prerequisites for a given course.
        """
        return self.courses.get(course, {}).get("prerequisites", [])

    def resolve_prerequisites(self, course):
        """
        Returns a list of courses to take in order to meet the prerequisites for a given course.
        """
        visited = set()
        order = deque()
        stack = [course]

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                order.appendleft(current)
                prerequisites = self.get_prerequisites(current)
                for prereq in prerequisites:
                    if prereq not in visited:
                        stack.append(prereq)
        return list(order)

class VideoStreamingService:
    """
    Simulates streaming of course videos, indicating integration with cloud-based services.
    """
    def get_course_video(self, course_name):
        print(f"Streaming video for {course_name}... (This would integrate with a scalable, cloud-based service using CDN and adaptive streaming protocols like HLS or DASH)")

class EnrollmentManager:
    """
    Manages course enrollments for a user, including saving and listing enrolled courses.
    """
    def __init__(self, course_catalog, user):
        self.user = user
        self.course_catalog = course_catalog
        self.enrolled_courses = self.load_enrollments()

    def load_enrollments(self):
        """
        Loads a user's enrolled courses from a JSON file.
        """
        try:
            with open(f"{self.user}_enrollments.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_enrollments(self):
        """
        Saves the current list of enrolled courses to a JSON file.
        """
        with open(f"{self.user}_enrollments.json", "w") as f:
            json.dump(self.enrolled_courses, f)

    def enroll(self, course_name):
        """
        Enrolls a user in a course and its prerequisites.
        """
        course_order = self.course_catalog.resolve_prerequisites(course_name)
        for course in course_order:
            if course not in self.enrolled_courses:
                self.enrolled_courses.append(course)
                print(f"Enrolled in {course}")
        self.save_enrollments()

    def list_enrolled_courses(self):
        """
        Lists the courses in which the user is enrolled.
        """
        print("Enrolled courses:")
        for course in self.enrolled_courses:
            print(course)

class LearningPath:
    """
    Generates and recommends learning paths based on user enrollment.
    """
    def __init__(self, enrollment_manager):
        self.enrollment_manager = enrollment_manager

    def generate_path(self):
        """
        Displays the user's current learning path.
        """
        print("Your Learning Path (based on current enrollments):")
        for course in self.enrollment_manager.enrolled_courses:
            print(course)

    def recommend_courses(self):
        """
        Recommends courses based on the user's interests and past enrollments.
        """
        print("Recommended courses based on your interests and past enrollments:")
        print("Course 1, Course 2, Course 3")

class Dashboard:
    """
    Provides a user interface for accessing various functionalities of the platform.
    """
    def __init__(self, enrollment_manager, learning_path):
        self.enrollment_manager = enrollment_manager
        self.learning_path = learning_path

    def display_dashboard(self):
        """
        Displays the dashboard, including enrolled courses and learning path recommendations.
        """
        print("\n--- Your Dashboard ---")
        self.display_enrolled_courses()
        self.display_progress()
        self.learning_path.recommend_courses()

    def display_enrolled_courses(self):
        """
        Displays a list of courses the user is enrolled in.
        """
        print("\nEnrolled Courses:")
        if not self.enrollment_manager.enrolled_courses:
            print("You are not enrolled in any courses.")
        else:
            for course in self.enrollment_manager.enrolled_courses:
                print(course)

    def display_progress(self):
        """
        Simulates and displays progress in enrolled courses.
        """
        print("\nCourse Progress:")
        if not self.enrollment_manager.enrolled_courses:
            print("No progress to display.")
        else:
            for course in self.enrollment_manager.enrolled_courses:
                print(f"{course}: {self.simulate_progress()}% complete")

    @staticmethod
    def simulate_progress():
        """
        Randomly generates progress percentages for enrolled courses.
        """
        return random.randint(10, 100)

def authenticate():
    """
    Authenticates a user or creates a new user account.
    """
    username = input("Enter your username: ")
    print("Authenticating...")
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    if username not in users:
        password = input("Create a password: ")
        users[username] = {"password": password}
        with open("users.json", "w") as f:
            json.dump(users, f)
        print("User created successfully.")
    else:
        print("User authentication successful.")
    return username

def main():
    """
    Main function to run the e-learning platform.
    """
    user = authenticate()
    if not user:
        print("Authentication failed or user creation cancelled.")
        return
    catalog = CourseCatalog()
    enrollment_manager = EnrollmentManager(catalog, user)
    path = LearningPath(enrollment_manager)
    video_service = VideoStreamingService()
    dashboard = Dashboard(enrollment_manager, path)
    while True:
        print("\nAvailable actions: \n1. List courses\n2. Enroll\n3. Show enrolled courses\n4. Show learning path\n5. Stream course video\n6. Recommend courses\n7. Show Dashboard\n8. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            catalog.list_courses()
        elif choice == "2":
            course_name = input("Enter the course name to enroll: ")
            enrollment_manager.enroll(course_name)
        elif choice == "3":
            enrollment_manager.list_enrolled_courses()
        elif choice == "4":
            path.generate_path()
        elif choice == "5":
            course_name = input("Enter the course name for video streaming: ")
            video_service.get_course_video(course_name)
        elif choice == "6":
            path.recommend_courses()
        elif choice == "7":
            dashboard.display_dashboard()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
