import random
def getInput():
    val=input("""enter 1 to generate unique password 
enter 0 to exit\n""")
    if(val=='1'):
        generatePassword(16)
    if(val=='0'):
        return "exiting"
def generatePassword(length=16):
    passw = []
    req={'u','l','d','s'}
    inc=set()

    while (len(passw) < length):

        ct=random.choice(['u','l','d','s'])
        if ct=='u':
            char=chr(random.randint(65,90))
        elif ct=='l':
            char=chr(random.randint(97,122))
        elif ct=='d':
            char=chr(random.randint(48,57))
        elif ct=='s':
            char=chr(random.randint(33,47))

        if char not in passw:
            passw.append(char)
            inc.add(ct)

    while req-inc:
        miss=(req-inc).pop()
        if miss=='u':
            char=chr(random.randint(65,90))
        elif miss=='l':
            char=chr(random.randint(97,122))
        elif miss=='d':
            char=chr(random.randint(48,57))
        elif miss=='s':
            char=chr(random.randint(33,47))
        
        if char not in passw:
            replace=random.randint(0,length-1)
            passw[replace]=char
            inc.add(miss)
    password=''
    for i in passw:
        password=password+i
    print("Your Unique Password-> " +password)
    getInput()

getInput()
    

