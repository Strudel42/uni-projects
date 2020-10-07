import matplotlib.pyplot as plt
import csv


def group_by(iterable, keySelector):

    # this function creates a dictionary from a list and groups them

    x = {}
    for i in iterable:
        key = keySelector(i)
        if key not in x:
            x[key] = []
        x[key].append(i)
    return x

outfile = open("EU_countries.csv","r")

file = csv.reader(outfile) #read in the file
next(file)
next(file, None)

plot = {}
grouped = group_by(file,lambda x: x[3]) # makes a dictionary of membership
for key in grouped:
    plot[key]=sum([*map(lambda x: int(x[1]), grouped[key])]) #maps the population to the key in 'grouped

outfile.close()

plt.title('EU population by member state')
#plot the pie chart
exploded = [0.1]*len(plot)
plt.pie(plot.values() ,labels = plot.keys(), startangle=45, rotatelabels=False,
        autopct='%1.1f%%', radius=1.2, explode=exploded, shadow=True)
plt.show()
