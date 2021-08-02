from abc import ABCMeta


# NOTE: This could also be done without metaclasses, but it seems more appropriate to use them, since __str__ is
#  returning the class name instead of the object name.
class PrintableABC(type(ABCMeta)):
    def __str__(self):
        return f"{self.__name__}"

    def __repr__(self):
        return self.__dict__
