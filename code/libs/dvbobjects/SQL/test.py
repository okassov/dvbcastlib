#import foo


def bar(a, b):

	c = a + b

	print (c)


handlers = {"bar": bar}


print (handlers["bar"](1,2))

