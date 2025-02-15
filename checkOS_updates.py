import os
import subprocess
import logging


Log_File=os.path.expanduser("~/PythonTraining/update_script.log")
logging.basicConfig(filename=Log_File,level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')
    
def scheduleUpdates():
    print("Scheduling automatic updates...")
    ipt=input("""choose update frequence:
1) Daily at 2 AM
2) Every Sunday at 3 AM
3) Every Hour
Choice: """)
    
    cron_job=""

    if ipt=='1':
        cron_job="0 2 * * * /usr/bin/python3 ~/PythonTraining/update_script.py >> ~/PythonTraining/update_script.log 2>&1"
    elif ipt=='2':
        cron_job="0 3 * * SUN /usr/bin/python3 ~/PythonTraining/update_script.py >> ~/PythonTraining/update_script.log 2>&1"  
    elif ipt=='3':
        cron_job="0 * * * * /usr/bin/python3 ~/PythonTraining/update_script.py >> ~/PythonTraining/update_script.log 2>&1"
    else:
        print("Invalid Choice. Cancelling Scheduling.")
        return "EXITING"
    try:
        subprocess.run(f'(crontab -l; echo "{cron_job}") | crontab -', shell=True, check=True)
        print("Automatic updates scheduled successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"failed to schedule updates: {e}")
        print("scheduling failed")

def getInput():
    subprocess.run("sudo apt update", shell=True, text=True, capture_output=True, check=True)
    while True:
        input1=input("""ENTER
1 to check updates,
2 to update all without checking
3 to schedule automatic updates
0 to exit:
Choice: """)
    
        if (input1=="1"):
            listUpdates()
        if(input1=='2'):
            updateAll()
        if(input1=='3'):
            scheduleUpdates()
        if(input1=='0'):
            return "EXITING!!!"
        

def listUpdates():
    try:
        stream = subprocess.run("sudo apt list --upgradable | awk -F'/' '{print $1}' | tail -n +2", shell=True, text=True, capture_output=True, check=True)
        output = [line.strip() for line in stream.stdout.split('\n') if line.strip()]

        if not output:

            print("no updates available")
            return "EXITING"
        else:
            print("Available Updates:\n")
            for i,line in enumerate(output,start=1):
                print(f"{i}){line}")

        updateMethod(output)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during listUpdates: {e}")
        print("Error during listUpdates:", e)

def updateMethod(output):
    while True:
        input2=input("""enter 0 to update all, 
enter index number to update specific upgradable available:\n""")
        if (input2=="0"):
            updateAll()
            break

        elif (input2.isdigit()):
            output_index=int(input2)-1
            if (0 <= output_index < len(output)):
                updatePackage(output[output_index]) 
                break
            else:
                print("Invalid Index. Enter Valid Index.")
        else:
            print("invalid input, enter a valid number")

def updateAll():
    try:
        result = subprocess.run("sudo apt upgrade -y", shell=True,text=True,capture_output=True)
        if result.returncode == 0:
            print("Update successful.")
        else:
            print("Update failed. Error")
            logging.error(f"Update failed to update all. Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Error during updateAll: {e}")
        print("Error during updateAll:", e)
    finally:
        return "EXITING"


def updatePackage(outputModule):
    try:
        cmd = f"sudo DEBIAN_FRONTEND=noninteractive apt install {outputModule} -y"
        stream = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        if (stream.returncode==0):
            print("update successful")
        else:
            print("update failed")
            logging.error(f"Update failed to update {outputModule}. Error: {stream.stderr}")
    except Exception as e:
        logging.error(f"Error during updating package chose: {e}")
        print("Error during updating one package:", e)
    finally:
        return "EXITING"

getInput()