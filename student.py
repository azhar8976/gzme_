#. Student Class:-
class Student:
    def __init__(self,name,marks):
        self.name = name
        self.marks = marks

    def grade(self):
        if self.marks >= 90:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 50:
            return "C"    
        else:
            return "C" 

    def percentage(self):
        return self.marks
        
    def display(self):
        print(f"Name: {self.name}")
        print(f"Marks: {self.marks}")
        print(f"Grade: {self.grade()}") 
        print(f"Percentage:", {self.percentage()}) 
s1 = Student("Azhar", 88)
s1.display()      


