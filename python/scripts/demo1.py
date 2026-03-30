import argparse

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("--input", type=str, required=True)
    parse.add_argument("--model", type=str, required=False, default="demo.pth")
    args = parse.parse_args()

    print("input: ", args.input)
    print("model: ", args.model)

if __name__ == "__main__":
    main()