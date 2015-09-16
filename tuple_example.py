__author__ = 'MilanAshara'

tuple_list=[("1",1),("2",2)]
print [tuple[1] for tuple in tuple_list]
print sum([tuple[1] for tuple in tuple_list])
s= "{0:.2f}".format((float(5)/15)*100)
print float(s)
if isinstance(s,basestring):
    print s