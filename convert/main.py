from convert.util.file_role import FileRole

# fr = FileRole(r'/home/l/PycharmProjects/daily-strutil/docs/input_data', r'/home/l/PycharmProjects/daily-strutil/docs'
#                                                                         r'/output_data')
fr = FileRole('docs/input_data', 'docs/output_data')
fr.read('\t')


def easy_sign(in_list):
    out_list = []
    for file in in_list:
        for line in file:
            out_list.append(line)
    return out_list


# print(type(easy_sign(range(1,15))))
# print(dir(easy_sign))

fr.write(easy_sign)
