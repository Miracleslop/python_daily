
from convert.util.file_role import FileRole

# fr = FileRole(r'/home/l/PycharmProjects/daily-strutil/docs/input_data', r'/home/l/PycharmProjects/daily-strutil/docs'
#                                                                         r'/output_data')
fr = FileRole('docs/input_data', 'docs/output_data')
fr.read('\t')


def easy_sign(in_list):
    out_list = []
    for li in [in_list]:
        pass
    return out_list

print(type(easy_sign(range(1,15))))

fr.write(easy_sign)
