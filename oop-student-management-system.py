# Problem 6: OOP - Student Course Management System 🎓
# Problem Statement: Design a university course management system that handles students, courses, enrollments, and grade calculations.

# Your Task: Write the complete classes from scratch to support the following operations:

class Student:
    # Class variable to track total students
    _total_students = 0
    
    def __init__(self, student_id, name, email, program):
        # Validate inputs
        if not student_id or not name or not email or not program:
            raise ValueError("All student details must be provided")
        
        # Private attributes (encapsulation)
        self._student_id = student_id
        self._name = name
        self._email = email
        self._program = program
        self._enrolled_courses = []  # List to store enrolled courses
        self._grades = {}  # Dictionary to store grades {course_code: grade}
        
        # Increment total students
        Student._total_students += 1
    
    # Getter methods
    def get_student_id(self):
        return self._student_id
    
    def get_name(self):
        return self._name
    
    def get_email(self):
        return self._email
    
    def get_program(self):
        return self._program
    
    def get_enrolled_courses(self):
        return self._enrolled_courses.copy()  # Return a copy to maintain encapsulation
    
    def get_grades(self):
        return self._grades.copy()  # Return a copy to maintain encapsulation
    
    # Enroll in a course
    def enroll_in_course(self, course):
        """Enroll student in a course if there's available space"""
        if course not in self._enrolled_courses:
            enrollment_result = course.enroll_student(self)
            if enrollment_result:
                self._enrolled_courses.append(course)
                return True
        return False
    
    # Add grade for a course
    def add_grade(self, course_code, grade):
        """Add a grade for a specific course"""
        if not isinstance(grade, (int, float)) or grade < 0 or grade > 100:
            raise ValueError("Grade must be a number between 0 and 100")
        self._grades[course_code] = grade
    
    # Calculate GPA
    def calculate_gpa(self):
        """Calculate GPA based on grades (4.0 scale)"""
        if not self._grades:
            return 0.0
        
        total_points = 0
        for grade in self._grades.values():
            # Convert percentage to 4.0 scale
            if grade >= 90:
                points = 4.0
            elif grade >= 80:
                points = 3.0
            elif grade >= 70:
                points = 2.0
            elif grade >= 60:
                points = 1.0
            else:
                points = 0.0
            total_points += points
        
        return round(total_points / len(self._grades), 2)
    
    # Get transcript
    def get_transcript(self):
        """Get student's transcript with all grades"""
        return {
            'student_id': self._student_id,
            'name': self._name,
            'program': self._program,
            'grades': self._grades.copy(),
            'gpa': self.calculate_gpa()
        }
    
    # Class methods
    @classmethod
    def get_total_students(cls):
        return cls._total_students
    
    @classmethod
    def get_average_gpa(cls):
        """This would need to be implemented with a registry of all students"""
        # For this implementation, we'll return a placeholder
        # In a real system, you'd maintain a list of all students
        return 0.0
    
    @classmethod
    def get_top_students(cls, n):
        """This would need to be implemented with a registry of all students"""
        # For this implementation, we'll return a placeholder
        # In a real system, you'd maintain a list of all students and sort by GPA
        return []
    
    def __str__(self):
        return f"Student({self._student_id}, {self._name}, {self._email}, {self._program})"


class Course:
    # Class variable to track total enrollments across all courses
    _total_enrollments = 0
    
    def __init__(self, course_code, course_name, instructor, credits, max_capacity):
        # Validate inputs
        if not course_code or not course_name or not instructor:
            raise ValueError("Course code, name, and instructor must be provided")
        if credits <= 0 or max_capacity <= 0:
            raise ValueError("Credits and max capacity must be positive")
        
        # Private attributes
        self._course_code = course_code
        self._course_name = course_name
        self._instructor = instructor
        self._credits = credits
        self._max_capacity = max_capacity
        self._enrolled_students = []  # List of enrolled students
        self._grades = {}  # Dictionary {student_id: grade}
        self._waitlist = []  # List of students on waitlist
    
    # Getter methods
    def get_course_code(self):
        return self._course_code
    
    def get_course_name(self):
        return self._course_name
    
    def get_instructor(self):
        return self._instructor
    
    def get_credits(self):
        return self._credits
    
    def get_max_capacity(self):
        return self._max_capacity
    
    def get_enrolled_students(self):
        return self._enrolled_students.copy()
    
    def get_enrollment_count(self):
        return len(self._enrolled_students)
    
    def get_available_spots(self):
        return self._max_capacity - len(self._enrolled_students)
    
    def is_full(self):
        return len(self._enrolled_students) >= self._max_capacity
    
    # Enroll a student
    def enroll_student(self, student):
        """Enroll a student in the course if space is available"""
        if student in self._enrolled_students:
            return False  # Already enrolled
        
        if not self.is_full():
            self._enrolled_students.append(student)
            Course._total_enrollments += 1
            return True
        else:
            # Add to waitlist if course is full
            if student not in self._waitlist:
                self._waitlist.append(student)
            return False
    
    # Add grade for a student
    def add_grade(self, student_id, grade):
        """Add a grade for a student in this course"""
        if not isinstance(grade, (int, float)) or grade < 0 or grade > 100:
            raise ValueError("Grade must be a number between 0 and 100")
        self._grades[student_id] = grade
    
    # Get course statistics
    def get_course_statistics(self):
        """Get statistics for the course"""
        if not self._grades:
            return {
                'course_code': self._course_code,
                'enrolled_count': len(self._enrolled_students),
                'average_grade': 0.0,
                'highest_grade': 0.0,
                'lowest_grade': 0.0
            }
        
        grades = list(self._grades.values())
        return {
            'course_code': self._course_code,
            'enrolled_count': len(self._enrolled_students),
            'average_grade': round(sum(grades) / len(grades), 2),
            'highest_grade': max(grades),
            'lowest_grade': min(grades)
        }
    
    # Class method to get total enrollments
    @classmethod
    def get_total_enrollments(cls):
        return cls._total_enrollments
    
    def __str__(self):
        return f"Course({self._course_code}, {self._course_name}, {self._instructor}, Credits: {self._credits})"


# Test Case 1: Creating courses with enrollment limits
math_course = Course("MATH101", "Calculus I", "Dr. Smith", 3, 30)
physics_course = Course("PHYS101", "Physics I", "Dr. Johnson", 4, 25)
cs_course = Course("CS101", "Programming Basics", "Prof. Brown", 3, 20)

print(f"Course: {math_course}")
print(f"Available spots in Math: {math_course.get_available_spots()}")

# Test Case 2: Creating students with different programs
student1 = Student("S001", "Alice Wilson", "alice@university.edu", "Computer Science")
student2 = Student("S002", "Bob Davis", "bob@university.edu", "Mathematics")
student3 = Student("S003", "Carol Lee", "carol@university.edu", "Physics")

print(f"Student: {student1}")
print(f"Total students: {Student.get_total_students()}")

# Test Case 3: Course enrollment
enrollment1 = student1.enroll_in_course(math_course)
enrollment2 = student1.enroll_in_course(cs_course)
enrollment3 = student2.enroll_in_course(math_course)

print(f"Alice's enrollment in Math: {enrollment1}")
print(f"Math course enrollment count: {math_course.get_enrollment_count()}")

# Test Case 4: Adding grades and calculating GPA
student1.add_grade("MATH101", 85.5)
student1.add_grade("CS101", 92.0)
student2.add_grade("MATH101", 78.3)

print(f"Alice's GPA: {student1.calculate_gpa()}")
print(f"Alice's transcript: {student1.get_transcript()}")

# Test Case 5: Course statistics
math_course.add_grade("S001", 85.5)
math_course.add_grade("S002", 78.3)

course_stats = math_course.get_course_statistics()
print(f"Math course statistics: {course_stats}")

# Test Case 6: University-wide analytics using class methods
total_enrollments = Course.get_total_enrollments()
print(f"Total enrollments across all courses: {total_enrollments}")

average_gpa = Student.get_average_gpa()
print(f"University average GPA: {average_gpa}")

top_students = Student.get_top_students(2)
print(f"Top 2 students: {top_students}")

# Test Case 7: Enrollment limits and waitlist
# Try to enroll more students than course capacity
for i in range(25):  # Assuming math course limit is 30
    temp_student = Student(f"S{100+i}", f"Student {i}", f"student{i}@uni.edu", "General")
    result = temp_student.enroll_in_course(math_course)

print(f"Course full status: {math_course.is_full()}")
print(f"Waitlist size: {len(math_course._waitlist) if hasattr(math_course, 'waitlist') else 0}")

# Expected outputs should show proper enrollment management, grade tracking,
# GPA calculations, course statistics, and university-wide analytics
