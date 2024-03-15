import os
import zipfile
import pathlib


#PGN_f = open("PGN_files\London2e6.pgn",'r')

def txtmaker(path):
    PGN_f = open(path,'r')
    PGN_out = open("PGNfile.txt",'a')
    lines = PGN_f.readlines()
    new_lines = []

    flag = 0
    total_games = 0
    for line in lines:
        line = list(line)
        if total_games >500:
            break
        if line[0] == '[':
            continue
        elif len(line) > 1:
            line[-1] = ' '
        elif line[0] == '\n':
            if flag == 1:
                flag-=1
                continue
            else:
                total_games+=1
                flag+=1
        line = "".join(line)
        new_lines.append(line)

    new_lines.remove('\n')
    #print(new_lines[0])
    PGN_out.writelines(new_lines)
    PGN_f.close()
    
for path in pathlib.Path("PGN_files").iterdir():
    if path.is_file():
        txtmaker(path)