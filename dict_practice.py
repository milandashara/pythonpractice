__author__ = 'milanashara'
dict=None
# if dict:
#     print "dict"
# else:
#     print " not dict"

list_test = [{"test": 1}, {"test": 4}, {"test": 3}, {"test": 2}, {"test":None},{"test": 5}]


list_test = sorted(list_test, key=lambda list_test: list_test['test'], reverse=True)
print list_test[:3]

if not "asd":
    print "test"

print "AB,CD".split(",")

print ",".join([])
expected_params ={}
def expected_params_1(x): [set(), lambda x: set(x.split(','))]
expected_params['include_carriers'] = expected_params_1("AB,CD")
print expected_params

v =[{"test"},{"test1"}]

for temp in v:
    print temp

test_dict = {"carriers":None}
if "carriers" in test_dict:
    print "test 1"

if test_dict.has_key("carriers") and test_dict["carriers"]:
    print "test 2"

print test_dict.get("s_code","")
if not test_dict.get("s_code",""):
    print "success"
if not None:
    print "success"

if not "":
    print "success"

for temp,value in test_dict.iteritems():
    print temp,value

