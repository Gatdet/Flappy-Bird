import logging

#logging levels allows us to specify what we want to log

#Debug: Detailed information, typically of in interest only when diagnosing problems

#INFO: Confirmation that everythong is working corrcetlu

#WARNING: An indication that something unexpectaed happend or will happen. Software still running

#ERROR: Due to more serious problem, the software has not been able to perform some function

#Critical: A serious error, indicating that the program itself may be unable to continue running

logging.basicConfig(filename="test.log", level=logging.DEBUG)

def add(x,y):
    return x+y

def sub(x,y):
    return x-y

def mul(x,y):
    return x*y

def div(x,y):
    return x/y

num1 = 20
num2 = 10

add_result = add(num1,num2)
logging.debug(f"Add {add_result}")

sub_resutl = sub(num1,num2)
logging.debug((f"Sub {sub_resutl}"))

mul_resutl = mul(num1,num2)
logging.debug((f"Mul {mul_resutl}"))


def containsDuplicate(nums):

    new = []

    for i in nums:
        if i in new:
            return True

        new.append(i)

    return False

print(containsDuplicate())
