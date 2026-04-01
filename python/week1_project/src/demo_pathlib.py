from pathlib import Path

base_dir = Path("/home/daydreamer/Desktop/study/python/week1_project")
intput_dir = base_dir / "input"
print("intput_dir is exist:", intput_dir.exists())
print("intput_dir is dir:", intput_dir.is_dir())
print("intput_dir is file:", intput_dir.is_file())
out_dir = base_dir / "output"
out_dir.mkdir(parents=True, exist_ok=True)
print("output_dir is exist:", out_dir.exists())
print("output_dir is dir:", out_dir.is_dir())
print("output_dir is file:", out_dir.is_file())

print("all intput_dir:")
for intput_name in intput_dir.iterdir():
    print(intput_name)

print("all intput_dir_name:")
for input_name in intput_dir.glob("*.png"):  #或者用.rglob("*.png")，它的作用是递归查找
    print(input_name)

print()
one = intput_dir / "test.png"
print(one.name)
print(one.stem)
print(one.suffix)
print(one.parent)

read_txt = intput_dir / "read_demo_pathlib.txt"
read_txt.write_text("""pathlib study:
Path()
/ 拼接路径                            
exists()                             
is_file()                            
is_dir()                             
mkdir()                              
iterdir()                            
rglob() or glob()                            
name                                 
stem                                 
suffix                               
parent                               
read_text()                          
write_text()""", encoding="utf-8")
content = read_txt.read_text()
print(content)