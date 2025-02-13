import os
import subprocess
import logging


Log_File=os.path.expanduser("~/PythonTraining/update_script.log")
logging.basicConfig(filename=Log_File,level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')
    
def getInput():
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
        if(input1=='0'):
            return "EXITING!!!"

def listUpdates():
    try:
        stream = subprocess.run("sudo apt list --upgradable | awk -F'/' '{print $1}' | tail -n +2", shell=True, text=True, capture_output=True, check=True)
        output = stream.stdout.split('\n')
        if not output or output == [""]:
            print("no updates available")
            return "EXITING"
        print("Available Updates:\n")
        for i,line in enumerate(output,start=1):
            print(f"{i}){line}")

        updateMethod(output)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during listUpdates: {e}")
        print("Error during listUpdates:", e)

def updateMethod(output):
    input2=input("""enter 0 to update all, 
enter index number to update specific upgradable available:\n""")
    if (input2=="0"):
        updateAll()
    elif (input2.isdigit()):
        output_index=int(input2)-1
        if (0 <= output_index < len(output)):
            outputModule=output[output_index].strip()
            updatePackage(outputModule)
        else:
            print("Invalid Index. Enter Valid Index.")
            updateMethod(output)
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
        stream = subprocess.run(f"sudo apt install {outputModule} -y",shell=True, text=True, capture_output=True )
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
# def getPackageName(input2):
#     stream1 = os.popen("sudo apt list --upgradable | awk -F'/' '{print $1}' | tail -n +2")
#     output1 = stream1.readlines()
#     j=1
#     for line in output1:
#         if(j==input2):
#             packageName=line
#             print(f"updating: {line} package")
#             break 
#         j=j+1
#     os.system(f'sudo apt install {packageName} -y')

getInput()