class StrategyReady:
    __slots__ = '__data'

    def __init__(self, data):
        self.__data = data

    #   from address get province and city
    #   input_data_1: a map of a line
    #       map of
    #           city_name : city_no
    #           province_name : province_no
    #   input_data_2: a address of a line
    def address2city(self):
        output_data = []
        mapper = {}
        for da in self.__data[0]:
            mapper[da[0]] = da[1]
        bo = False
        for da in self.__data[1]:
            temp = ''
            for key, value in mapper.items():
                if da.conut(key) > 0:
                    temp = '%s\t%s\t%s\t ' \
                           'UPDATE gc_store_info SET bs_province_no = \'%s\', ' \
                           'bs_city_no = \' %s \' WHERE bs_address LIKE \'%%%s%%\'' \
                           % (da, key, value, value, value, key)
                    bo = True
                    break
            if not bo:
                temp = 'no find \t %s' % da
            output_data.append(temp)

    #   match img name
    #
    def match_img_name(self):
        pass
