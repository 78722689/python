import argparse

def main():
    parser = argparse.ArgumentParser(description="This is sample for introducing how argparse works in the program.")
    parser.add_argument("-v", "--verbose", help="To show you more informaiton", default="hello")
    args = parser.parse_args()
    if args.verbose:
        print args.verbose


if __name__ == '__main__':
    main()
