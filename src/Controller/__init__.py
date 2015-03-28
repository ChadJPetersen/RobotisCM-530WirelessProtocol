import os

print("hello ACM\nWhat is your name??")
 
exitBool = True
    

def talk():
    print("I'm sorry, " + name + ", but I can't do that")
    anyKey1 = raw_input("\nPress any key to continue...")
    os.system("clear")
    
    
name = raw_input()
print("Well hello there.")



while(exitBool):
    print("\n\n\n\nWhat can I do for you, " + name + "?\n")
    print(" 1. Create your robot interface for you\n")
    print(" 2. Exit \n")
    n = int(input("Answer: "))
    
    if n == 1:
        talk()
    elif n == 2:
        exitBool = False
    else:
        print "I'm sorry, but " + n + " is not an answer"