import pandas

data = {
    'id': [101,102,103,104],
    'name': ['Prakash','Sahil','Ajay','Mayur'],
    'city': ['Rajkot','Surat','Baroda','Pune']
}

dt = pandas.DataFrame(data)
print(dt)