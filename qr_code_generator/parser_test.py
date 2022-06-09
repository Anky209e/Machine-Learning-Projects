import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--users",type=str,nargs=2,required=True)

args = parser.parse_args()

print(args.users)