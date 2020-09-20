import os 

titles_folder = "final_index/titles"
if not os.path.exists(titles_folder):
    os.mkdir(titles_folder)

THRESHOLD = 2000

cur_title_file_no = 0
titles_count = 1
f  = open("titles.txt")
cur_title_file = open(os.path.join(titles_folder, str(cur_title_file_no) + ".txt"), "w")

while True:
    line = f.readline()
    if not line:
        break 
    cur_title_file.write(line)
    titles_count += 1
    if not titles_count % THRESHOLD:
        cur_title_file_no += 1
        cur_title_file = open(os.path.join(titles_folder, str(cur_title_file_no) + ".txt"), "w")

