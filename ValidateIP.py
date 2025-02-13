import re
def publicORprivate(ip,listOctals):
    
    if(listOctals[0]=='10'):
        
        print("Type: Private IP")
        takeIP()
    elif(listOctals[0]=='172' and (int(listOctals[1])>=16 and int(listOctals[1])<=31)):
        
        print("Type: Private IP")
        takeIP()
    elif(listOctals[0]=='192' and listOctals[1]=='168'):
        
        print("Type: Private IP")
        takeIP()
    elif(listOctals[0]=='127'):
        
        print("Type: Reserved IP")
        takeIP()
    elif(listOctals[0]=='169' and listOctals[1]=='254'):
        print("Type: APIPA")
        takeIP()
    elif(listOctals[0]=='100' and (int(listOctals[1])>=64 and int(listOctals[1])<=127)):
        print("Type: CGNAT Reserved")
        takeIP()
    else:
        print("Type: Public IP")
        takeIP()
    

def takeIP():
    print("enter 0 to exit")
    ip=input("enter ip or gmail address for validation:")
    validateEmail(ip)
    
def validateEmail(ip):
    if(ip=='0'):
        print("exiting")
        return
    elif (re.match(r'^[0-9.]+$', ip)):
        ValidateIP(ip)
    else:
        if(ip.count("@gmail.com")==1):
            if ip.endswith("@gmail.com"):  
                i = 0
                valid = True  

                while ip[i] != '@':  
                    char_code = ord(ip[i])

                    if 65 <= char_code <= 90: 
                        print("Invalid Email: Capital letter in G-mail Address")
                        valid = False
                        takeIP()
                    elif 32 <= char_code <= 44 or 46 <= char_code <= 47 or 58 <= char_code <= 64 or 91 <= char_code <= 96 or 123 <= char_code <= 127:
                        print("Invalid Special Character in Email")
                        valid = False
                        takeIP()
                    i += 1  

                if valid:
                    print("Email Format Correct!")
                    takeIP()
        else:
            print("Invalid Email Address of Different Domain")
            takeIP()
   
def ValidateIP(ip):
        count_dot=ip.count(".")
        if(count_dot==3):
            listOctals=ip.split('.')
            
            if(len(listOctals)==4):
                for i in listOctals:
                    j=int(i)
                    if (j<0 or j>255):
                        print("invalid IP")
                        return takeIP()
                print("valid ip, congratulations!")
                print("wait, checking ipv4 type... ")
                publicORprivate(ip,listOctals)
            else:
                print("invalid ipv4 format")
                return takeIP()
        else:
            print("invalid ipv4 address format,Enter again")
            return takeIP()

takeIP()
