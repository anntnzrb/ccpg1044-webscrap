import csv


def merge_csvs(filenames: list[str], output_filename: str):
    with open(output_filename, 'w', encoding='utf-8', newline='') as output_file:
        writer = csv.writer(output_file, delimiter='|')

        for filename in filenames:
            with open(filename, 'r', encoding='utf-8') as input_file:
                reader = csv.reader(input_file, delimiter='|')

                if input_file.tell() == 0:
                    writer.writerow(next(reader))

                for row in reader:
                    writer.writerow(row)


if __name__ == '__main__':
    filenames = ['../data/guayas.csv', '../data/manabi.csv',
                 '../data/pichincha.csv', '../data/santa-elena.csv']
    output_filename = '../data/computrabajo.csv'
    merge_csvs(filenames, output_filename)
