def a():
	def b():
		def c():
			def d():
				x = 20
				print('d() says', x)
			print('c() says', x)
			d()
		print('b() says', x)
		c()
	x = 15
	print('a() says', x)
	b()

x = 10
print('main says', x)
a()

