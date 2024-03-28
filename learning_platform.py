import json
import random
from collections import deque
import pandas as pd
import sklearn
import networkx as nx

class CourseCatalog:
    """Manages the course catalog, including loading courses from a file, building a course prerequisite graph,
    and listing courses with their descriptions."""
    
    def __init__(self):
        self.courses = self.load_courses()  # Load courses from a JSON file or initialize with a default set
        self.graph = self.build_course_graph()  # Construct a directed graph of course prerequisites

    def load_courses(self):
        """Loads course data from a JSON file. If the file is not found, returns a default set of courses."""
        try:
            with open("courses.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Default course set provided for initial usage or in case of missing file
            return {
                "Python Basics": {"prerequisites": [], "description": "Learn the fundamentals of Python programming."},
                "Introduction to Programming": {"prerequisites": [], "description": "An introductory course for programming concepts."},
                "Data Structures": {"prerequisites": ["Python Basics"], "description": "Explore data structures in Python."},
                "Algorithms": {"prerequisites": ["Data Structures"], "description": "Learn about algorithms and their applications."},
                "Machine Learning": {"prerequisites": ["Python Basics", "Data Structures", "Statistics"], "description": "Dive into the basics of machine learning."},
            }

    def build_course_graph(self):
        """Builds a directed graph representing course prerequisites using NetworkX."""
        G = nx.DiGraph()
        for course, details in self.courses.items():
            G.add_node(course)  # Each course is a node in the graph
            for prerequisite in details["prerequisites"]:
                G.add_edge(prerequisite, course)  # Create an edge from prerequisite to course
        return G

    def list_courses(self):
        """Prints a list of all courses with their descriptions."""
        for course, details in self.courses.items():
            print(f"{course}: {details.get('description', 'No description')}")

    def get_prerequisites(self, course):
        """Returns a list of prerequisites for a given course."""
        return self.courses.get(course, {}).get("prerequisites", [])

    def resolve_prerequisites(self, course):
        """Resolves and returns an ordered list of courses to fulfill the prerequisites of the specified course.
        If a circular dependency is detected, raises a ValueError."""
        if nx.is_directed_acyclic_graph(self.graph):
            return list(nx.topological_sort(self.graph))  # Returns courses in an order respecting prerequisites
        else:
            # Handling circular dependencies
            try:
                cycle = nx.find_cycle(self.graph, orientation='original')
                raise ValueError(f"Course dependencies form a cycle! Detected cycle: {cycle}. Try re-evaluating the prerequisites.")
            except nx.NetworkXNoCycle:
                return []

class VideoStreamingService:
    """Handles streaming of course videos. Future implementations could integrate CDN usage and adaptive bitrate streaming for scalability and performance."""
    
    def __init__(self):
        # Placeholder for initializing streaming service components
        pass

    def get_course_video(self, course_name):
        """Simulates streaming a video for the specified course. Implementation for CDN and adaptive bitrate streaming could be added here."""
        print(f"Streaming video for {course_name}...")

class EnrollmentManager:
    """Manages course enrollments for a user, including loading and saving enrollments to a file."""
    
    def __init__(self, course_catalog, user):
        self.user = user
        self.course_catalog = course_catalog
        self.enrolled_courses = self.load_enrollments()  # Load user's enrollments from a file

    def load_enrollments(self):
        """Loads the user's enrolled courses from a JSON file. If the file is not found, returns an empty list."""
        try:
            with open(f"{self.user}_enrollments.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_enrollments(self):
        """Saves the user's current enrolled courses to a JSON file."""
        with open(f"{self.user}_enrollments.json", "w") as f:
            json.dump(self.enrolled_courses, f)

    def enroll(self, course_name):
        """Enrolls the user in the specified course and its prerequisites. Handles circular dependency errors."""
        try:
            course_order = self.course_catalog.resolve_prerequisites(course_name)
            for course in course_order:
                if course not in self.enrolled_courses:
                    self.enrolled_courses.append(course)
                    print(f"Enrolled in {course}")
            self.save_enrollments()
        except ValueError as e:
            print(e)

    def list_enrolled_courses(self):
        """Prints a list of courses the user is currently enrolled in."""
        print("Enrolled courses:")
        for course in self.enrolled_courses:
            print(course)

class LearningPath:
    """Generates and recommends learning paths for the user. Future versions could use machine learning to personalize recommendations."""
    
    def __init__(self, enrollment_manager):
        self.enrollment_manager = enrollment_manager

    def generate_path(self):
        """Generates a learning path based on the user's current enrollments. Placeholder for a more dynamic approach."""
        print("Your Learning Path (based on current enrollments):")
        for course in self.enrollment_manager.enrolled_courses:
            print(course)

    def recommend_courses(self):
        """Recommends courses to the user based on their interests and past enrollments. Placeholder for machine learning-based recommendations."""
        print("Recommended courses based on your interests and past enrollments:")
        # Placeholder for recommendation logic
        print("Course 1, Course 2, Course 3")

class Dashboard:
    """Presents a dashboard to the user, including enrolled courses, course progress, and recommended courses."""
    
    def __init__(self, enrollment_manager, learning_path):
        self.enrollment_manager = enrollment_manager
        self.learning_path = learning_path

    def display_dashboard(self):
        """Displays the user's dashboard, including enrolled courses, progress, and recommendations."""
        print("\n--- Your Dashboard ---")
        self.display_enrolled_courses()
        self.display_progress()
        self.learning_path.recommend_courses()

    def display_enrolled_courses(self):
        """Displays a list of the user's enrolled courses."""
        print("\nEnrolled Courses:")
        if not self.enrollment_manager.enrolled_courses:
            print("You are not enrolled in any courses.")
        else:
            for course in self.enrollment_manager.enrolled_courses:
                print(course)

    def display_progress(self):
        """Displays the user's progress in each enrolled course. Placeholder for a future implementation considering various internet speeds and high traffic."""
        print("\nCourse Progress:")
        if not self.enrollment_manager.enrolled_courses:
            print("No progress to display.")
        else:
            for course in self.enrollment_manager.enrolled_courses:
                print(f"{course}: {random.randint(10, 100)}% complete")

def authenticate():
    """Handles user authentication, including user creation if necessary."""
    username = input("Enter your username: ")
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
    """Main function to run the application. Handles user interaction and navigation through the platform."""
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
        action = input("\nAvailable actions: \n1. List courses\n2. Enroll\n3. Show enrolled courses\n4. Show learning path\n5. Stream course video\n6. Recommend courses\n7. Show Dashboard\n8. Exit\nEnter your choice: ")
        if action == "1":
            catalog.list_courses()
        elif action == "2":
            course_name = input("Enter the course name to enroll: ")
            enrollment_manager.enroll(course_name)
        elif action == "3":
            enrollment_manager.list_enrolled_courses()
        elif action == "4":
            path.generate_path()
        elif action == "5":
            course_name = input("Enter the course name for video streaming: ")
            video_service.get_course_video(course_name)
        elif action == "6":
            path.recommend_courses()
        elif action == "7":
            dashboard.display_dashboard()
        elif action == "8":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
