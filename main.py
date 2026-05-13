import os 
from pathlib import Path

def createfolder():
    name = input("please tell your folder name: ")
    p = Path(name)
    if not p.exists():
        p.mkdir()
    else:
        print("folder name already exists ")

def listingfoldersandfile():
    p = Path('')
    items = list(p.rglob('*'))
    for i,v in enumerate(items):
        print(f"{i+1} : {v}")

def updatefolder():
    listingfoldersandfile()
    oname = input("which folder you want to update : ")
    old_p = Path(oname)
    if old_p.exists():
        n_name = input("tell folders new name: ")
        new_p = Path(n_name)
        if not new_p.exists():
            old_p.rename(new_p)
        else:
            print("this name folder already exist ")

    else:
        print("no such folder name exists ")

def deletefolder():
    listingfoldersandfile()
    name = input("which folder you want to delete: ")
    p = Path(name)
    if p.exists():
        p.rmdir()
    else:
        print("no such folder exists ")

def createfile():
    name = input("tell your file name with extension :- ")
    p = Path(name)
    if not p.exists():
        with open(p,"w") as file:
            data = input("what you want to write inside :- ")
            file.write(data)
            print("created successfully ")
    else:
        print("this file already exists ")
    
def readfile():
    listingfoldersandfile()
    name = input("which file you want to read write with extension :- ")
    p = Path(name)
    if p.exists and p.is_file():
        with open(p,'r') as file:
            data = file.read()
            print(data)
        print("file read successfull")
    else:
        print("no such file exists")
        
def updatefile():
    listingfoldersandfile()
    name = input("which file you want to update :- ")
    p = Path(name)
    if p.exists() and p.is_file():
        print("press 1 for updating the file name :- ")
        print("press 2 for overwriting the content :- ")
        print("press 3 for appending in file :- ")
        check = int(input("tell your response :- "))
        if check == 1:
            new_name = input("tell your new name :- ")
            new_p = Path(new_name)
            if not new_p.exists():
                p.rename(new_p)
                print("name updated successfully ")
            else:
                print("this name already exists ")
        if check == 2:
            with open(p,'w') as file:
                data = input("what you want to overwrite :- ")
                file.write(data)
                print("updated successfully")
        if check == 3:
            with open(p,'a') as file:
                data = input("what you want to append :- ")
                file.write(" "+ data)
                print("updated successfully")
    else:
        print("no such file exists ")

def deletefile():
    listingfoldersandfile()
    name = input("which file you want to delete:- ")
    p = Path(name)
    if p.exists() and p.is_file():
        os.remove(p)
        print("file deleted successfully")
    else:
        print("no such file exists ")



while True:
    print("press 1 for creating a folder")
    print("press 2 for Listing files and folders")
    print("press 3 for updating a folder name")
    print("press 4 for deleting a folder ")
    print("press 5 for creating a file")
    print("press 6 for reading a file ")
    print("press 7 for updating a file")
    print("press 8 for deleting a file")
    print("press 0 to exit the application ")

    res = int(input("tell your response:- "))

    if res == 1:
        createfolder()

    if res == 2:
        listingfoldersandfile()

    if res == 3:
        updatefolder()

    if res == 4:
        deletefolder()

    if res == 5:
        createfile()

    if res == 6:
        readfile()

    if res == 7:
        updatefile()

    if res == 8:
        deletefile()
    
    if res == 0:
        break



    






































# from pathlib import Path

# def readfielandfolder():
#     path = Path('')
#     items = list(path.rglob('*'))
#     for i, item in enumerate(items):
#         print(f"{i+1} : {item}")


# def createfile():
#     try:
#         readfielandfolder()
#         name = input("please tell your file name :- ")
#         p = Path(name)

#         if not p.exists():
#             with open(p, "w") as fs:
#                 data = input("what you want to write in this file :- ")
#                 fs.write(data)

#             print("FILE CREATED SUCCESSFULLY")
#         else:
#             print("this file already exist")

#     except Exception as err:
#         print(f"An error occured as {err}")


# def readfile():
#     try:
#         readfielandfolder()
#         name = input("which file you want to read :- ")
#         p = Path(name)

#         if p.exists() and p.is_file():
#             with open(p, 'r') as fs:
#                 data = fs.read()
#                 print("\n----- FILE CONTENT -----")
#                 print(data)
#                 print("------------------------")

#             print("Readed successfully")
#         else:
#             print("the file does not exist")

#     except Exception as err:
#         print(f"An error occured as {err}")


# def updatefile():
#     try:
#         readfielandfolder()
#         name = input("which file you want to update :- ")
#         p = Path(name)

#         if p.exists() and p.is_file():
#             with open(p, 'a') as fs:
#                 data = input("what you want to add in file :- ")
#                 fs.write("\n" + data)

#             print("FILE UPDATED SUCCESSFULLY")
#         else:
#             print("the file does not exist")

#     except Exception as err:
#         print(f"An error occured as {err}")


# def deletefile():
#     try:
#         readfielandfolder()
#         name = input("which file you want to delete :- ")
#         p = Path(name)

#         if p.exists() and p.is_file():
#             p.unlink()
#             print("FILE DELETED SUCCESSFULLY")
#         else:
#             print("the file does not exist")

#     except Exception as err:
#         print(f"An error occured as {err}")


# print("press 1 for creating a file")
# print("press 2 for reading a file")
# print("press 3 for updating a file")
# print("press 4 for deleting a file")

# check = int(input("please tell your response :- "))

# if check == 1:
#     createfile()

# elif check == 2:
#     readfile()

# elif check == 3:
#     updatefile()

# elif check == 4:
#     deletefile()

# else:
#     print("Invalid choice")



# FILE HANDLING:-
# mode: r - read, w - write
# open file

# file = open('example.txt', 'r')


# read file

# file = open('example.txt', 'r')
# content = file.read() # read entire data
# print(content)
# file.close() #best practice

# file = open('example.txt', 'r')
# content = file.read() # read first line
# print(content)
# file.close() 

# file = open('example.txt', 'r')
# content = file.read() # list entire data
# print(content)
# file.close() 









