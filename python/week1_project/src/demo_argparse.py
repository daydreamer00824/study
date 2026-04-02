import argparse

parse = argparse.ArgumentParser(description="argparse study")

parse.add_argument("parent_dir", type=str, help="input parent dir")
parse.add_argument("--input_dir", type=str, required=True, help="input the input dir")
parse.add_argument("--output_dir", type=str, required=True)

parse.add_argument("--model", type=str, choices=["train, test, val"], default="train")
parse.add_argument("--epoch", type=int, default=10)
parse.add_argument("--lr", type=float, default=0.001)
parse.add_argument("--gpu", action="store_true")

arg = parse.parse_args()

print(arg.parent_dir)
print(arg.input_dir)
print(arg.output_dir)
print(arg.model)
print(arg.epoch)
print(arg.lr)
print(arg.gpu)

