import csv
import json

input_file_name = 'user_choice_movie50.csv'
output_file_name = 'user_choice_movie50.txt'

with open(input_file_name, 'r', encoding="utf-8", newline="") as input_file, \
    open(output_file_name, "w", encoding="utf-8", newline="") as output_file:

    reader = csv.reader(input_file)
    num = 1

    col_names = next(reader)
    output_file.write('[\n')
    for cols in reader:
        output_file.write('\t{\n')
        output_file.write('\t\t\"pk\": {},\n'.format(num))
        num += 1
        output_file.write('\t\t\"model\": \"movies.movie\",\n')
        output_file.write('\t\t\"fields\": \n')
        # doc = {}
        # for col_name, col in zip(col_names, cols):
        #     if col_name == 'MovieCd' or col_name == 'pubDate':
        #         doc[col_name] = int(col)
        #     elif col_name == 'userRating':
        #         doc[col_name] = float(col)
        #     doc[col_name] = col
        doc = {col_name: col for col_name, col in zip(col_names, cols)}
        print(json.dumps(doc, ensure_ascii=False), file=output_file)
        output_file.write('},\n')
    output_file.write(']\n')

    