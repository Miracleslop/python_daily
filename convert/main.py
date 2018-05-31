
from convert.util.file_role import FileRole

# fr = FileRole(r'/home/l/PycharmProjects/daily-strutil/docs/input_data', r'/home/l/PycharmProjects/daily-strutil/docs'
#                                                                         r'/output_data')
fr = FileRole(r'docs/input_data', r'docs/output_data')
fr.read('\t')


def easySign(inlist, outlist):
    for row in inlist:
        for cel in row:
            outlist.append(cel)


fr.write('1', easySign)
