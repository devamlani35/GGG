import os

if __name__ == "__main__":
    directory = ""
    with open("text_load.txt") as f:
        yeses = list(map(lambda x: x+".tar", list(map(str.strip,f.readlines()))))
    print(yeses)
    os.chdir(directory)
    for val in os.listdir():
        label = "No"
        if val in yeses:
            label = "Yes"
    
