__author__ = 'MilanAshara'

import pprint, pickle
# data1 = {'a': [1, 2.0, 3, 4+6j],
#          'b': ('string', u'Unicode string'),
#          'c': None}
# selfref_list = [1, 2, 3]
# selfref_list.append(selfref_list)
# output = open('data.pkl', 'wb')
# # Pickle dictionary using protocol 0.
# pickle.dump(data1, output)
pkl_file = open('data.pkl', 'rb')

data1 = pickle.load(pkl_file)
pprint.pprint(data1)