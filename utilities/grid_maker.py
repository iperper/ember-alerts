import numpy

y_t = 38.290
y_b = 37.466
x_r = -121.212
x_l = -122.726

t = 0
for x in numpy.arange(x_l, x_r, .06):
    for y in numpy.arange(y_b, y_t, .04):
        print(str(x)+','+str(y))
        t+=1
print(t)
