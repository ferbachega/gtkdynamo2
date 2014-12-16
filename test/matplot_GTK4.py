# definitions for the axes
left, width = 0.1, 0.85 #0.65
bottom, height = 0.1, 0.85 #0.65
bottom_h = left_h = left+width+0.02

rect_scatter = [left, bottom, width, height]

# start with a rectangular Figure
fig = plt.figure(1, figsize=(8,8))
axScatter = plt.axes(rect_scatter)

# the scatter plot:
p1 = axScatter.scatter(x[0], y[0], c='blue', s = 70)
p2 = axScatter.scatter(x[1], y[1], c='green', s = 70)
p3 = axScatter.scatter(x[2], y[2], c='red', s = 70)
p4 = axScatter.scatter(x[3], y[3], c='yellow', s = 70)
p5 = axScatter.plot([1,2,3], "r--")

plt.legend([p1, p2, p3, p4, p5], [names[0], names[1], names[2], names[3], "Random guess"], loc = 2)

# now determine nice limits by hand:
binwidth = 0.25
xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
lim = ( int(xymax/binwidth) + 1) * binwidth

axScatter.set_xlim( (-lim, lim) )
axScatter.set_ylim( (-lim, lim) )

xText = axScatter.set_xlabel('FPR / Specificity')
yText = axScatter.set_ylabel('TPR / Sensitivity')

bins = np.arange(-lim, lim + binwidth, binwidth)
plt.show()
