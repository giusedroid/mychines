
def logit( f, pre, post):
	def target(*args):
		print pre
		f(*args)
		print post
	return target

def log(v, *s):
	if v:
		print " ".join( str(ss) for ss in s)
