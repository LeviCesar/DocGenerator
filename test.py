class Geeks:
    def __init__(self):
        self.__age = 0
    
    # using property decorator
    # a getter function
    @property
    def age(self):
        print("getter method called")
        return self.__age
    
    # a setter function
    @age.setter
    def age(self, a):
        if(a < 18):
            raise ValueError("Sorry you age is below eligibility criteria")
        print("setter method called")
        self.__age = a
  
mark = Geeks()
  
mark.age = 19
  
print(mark.age)