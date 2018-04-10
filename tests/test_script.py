from cidc_utils.requests import SmartFetch

s = SmartFetch('http://localhost:5000')

a = s.post(code=201, url='test', json={'message': 'hi'})

print(a)

b = a()

print(b)

