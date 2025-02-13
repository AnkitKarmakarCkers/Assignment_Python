import os
def listUpdates():
    stream = os.popen("sudo apt list --upgradable | awk -F'/' '{print $1}' | tail -n +2")
    output = stream.readlines()
    #print(output)
    i=1
    for line in output:
        print(f"{i}){line}") 
        i=i+1
listUpdates()
