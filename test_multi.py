import argparse

if __name__ == '__main__':
    # Парсим аргументы

    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)

    args = parser.parse_args()
    stroka = args.list

    print(stroka)