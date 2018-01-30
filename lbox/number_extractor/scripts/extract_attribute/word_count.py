import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-keyword", type=str, help="The keyword to be searched.", default="more than")    
    parser.add_argument("-ifnames", nargs='+', help="The data files to be opened.", default=None)
    args = parser.parse_args()

    ifnames = args.ifnames
    keyword = args.keyword
    word_count = {}
    for fname in ifnames:
        cnt = 0
        with open(fname) as ifile:
            print("Processing {}".format(fname))

            for line in ifile:
                if keyword in line:
                    cnt += 1
            word_count[fname] = cnt
    print(word_count)
