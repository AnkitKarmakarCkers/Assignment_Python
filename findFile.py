
import hashlib
import os

def make_hash(path):
    hasher = hashlib.sha256()
    with open(path, 'rb') as file:
        
        chunk = 0
        while chunk != b'':
            
            chunk = file.read(1024)
            hasher.update(chunk)
    return hasher.hexdigest()

def search_dublicates_in_dir(directory):
    file_hashes = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = make_hash(file_path)
                                      
                                      
            if file_hash:  
                file_hashes.setdefault(file_hash, []).append(file_path)

    
    duplicates = {}

    for file_hash, paths in file_hashes.items():
        if len(paths) > 1: 
            duplicates[file_hash] = paths

    return duplicates

def list_duplicates(duplicates):
    duplicate_map = {}

    index = 1  
    for file_hash, paths in duplicates.items():
        print("\n  Hash: " + file_hash)  

        for path in paths:
            print(f"  [{index}] {path}")  
            duplicate_map[index] = path  
            index+=1
    return duplicate_map
    


while(True):
    duplicate_map = list_duplicates(search_dublicates_in_dir("/home/ankit/Assignment_Python/"))
    
    if(len(duplicate_map) == 0):
        print("NO DUPLICATES")
        break
    
    print("Enter 0 to exit")
    
    choice = int(input("Enter the index of the file to delete: "))
    if(choice == 0):
        break
    if(choice in duplicate_map):
        os.remove(duplicate_map[choice])
        print("File deleted successfully.")
        break
    else:
        print("Invalid choice. Please enter a valid index.")
