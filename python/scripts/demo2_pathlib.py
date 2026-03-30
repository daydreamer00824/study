from pathlib import Path

data_dir = Path("xx/xx")
print(data_dir)

print(data_dir.exists())  #exist?
print(data_dir.is_dir())  #is dir or not

out_dir = Path("xx/xx/xx")
out_dir.mkdir(exist_ok=True)  # if exist: do not tell me error

files = list(data_dir.glob("*.jpg"))

print(files)
print(len(files))

#data_dir.name:xx
#data_dir.stem:xx
#data_dir.suffix:.jpg


#批量处理

for file_path in files:
    print(file_path)

#save

save_path = out_dir / file_path.name  # /不是除法,在Path里表示路劲拼接
print(save_path)