"""
This is a module for checking various linting rules.
"""

pascalCase = "Case of Pascal"
snake_case = "case_of_snake"

class SomeClass:
    """ Class that does stuff """
    def __init__(self):
        hey_you = "0"
        isTrue = False
        if hey_you:
            isTrue = hey_you
        print(isTrue)


    def DoStuff(self, thing):
        return thing

someInstance = SomeClass()

exit()