import os
import time
import sys
import select

def interrupt():
    print("Press Enter to stop check",end='',flush=True)
    sys.stdin.readline()
    print("Returning to console")
    raise KeyboardInterrupt

def takeInput():
    
    url = input("Enter URLs of your choice or enter 0 to exit: ")
    if(url=="0"):
        return "exiting"
    CheckUrls(url)

#
def CheckUrls(url):
    try:
        while True:
            urls = url.split()
            for url in urls:
                print(f"Your url {url} status is:")
                    
                response = os.popen(f"curl -I -s {url}").read()
                lines = response.splitlines()

                if not lines:
                    print("Error: No response received!")
                    continue

                status_line = lines[0]

                if status_line.startswith(("HTTP/1.1 200", "HTTP/2 200")):
                    print("HEALTHY URL RESPONSE")
                    print(status_line)

                elif status_line.startswith("HTTP/1.1 301"):
                    print("Do you mean: ")
                        
                    correctURL = None
                    for line in lines:
                        if line.lower().startswith("location:"):
                            correctURL = line.split(":", 1)[1].strip()
                            break
                        
                    if correctURL:
                        print(f"{correctURL} ?")
                        print(f"If yes, then status check for {correctURL} is: ")

                        redirect_response = os.popen(f"curl -I -s {correctURL}").read()
                        redirect_status_line = redirect_response.splitlines()[0] if redirect_response else "No response"

                        if redirect_status_line.startswith(("HTTP/1.1 200", "HTTP/2 200")):
                            print("HEALTHY URL RESPONSE")
                            print(redirect_status_line)
                        else:
                            print("UH OH! UNHEALTHY URL RESPONSE! STATUS:")
                            print(redirect_status_line)
                    else:
                        print("Error: Could not determine the redirected URL.")

                else:
                    print("UH OH! UNHEALTHY URL RESPONSE! STATUS:")
                    print(status_line)

            print("Running check on url every 5 second. Press 0 to exit.") 
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting back to console")
        return


takeInput()
