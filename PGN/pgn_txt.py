import zipfile
import pathlib
import os



for filename in enumerate(os.listdir("PGN_files")):
        #dst ="Hostel" + str(count) + ".jpg"
        #src ='xyz'+ filename
        #dst ='xyz'+ dst
        #print(filename[1])
        path_as_list = list(filename[1])
        path_as_list[-1] = 't'
        path_as_list[-2] = 'x'
        path_as_list[-3] = 't'
        new_name = "".join(path_as_list)
        src = "PGN_files\\" + filename[1]
        dst = "PGN_files\\" + new_name
        os.rename(src,dst)
        
          
        # rename() function will
        # rename all the files
        #os.rename(src, dst)

# for path in pathlib.Path("PGN_files").iterdir():
#     if path.is_file():
#         path_as_list = list(path)
#         path_as_list[-1] = 't'
#         path_as_list[-2] = 'x'
#         path_as_list[-3] = 't'
#         path_new = "".join(path_as_list)
#         os.rename(path,path_new)
        