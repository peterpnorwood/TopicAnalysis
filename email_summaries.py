#### OTHER RANDOM ITEMS IN THE MEMO-LIST ANALYSIS ####

### Finding the Top memo-list threads of all time and of from each year

grp = emails.groupby(["subjects"]).size().reset_index(name='count')
grp = grp.sort_values('count',ascending=False)[0:10]
print("Most Popular memo-list Threads of All Time")
print(grp)

## ------------------------------------------------------------------------------------ ##

for i in range(1998,2019):
    year = emails[emails.year == i]
    grp = year.groupby(["subjects"]).size().reset_index(name='count')
    grp = grp[['count','subjects']]
    grp = grp.sort_values('count',ascending=False)[0:10]
    print("Most Popular memo-list Threads in %d" % (i))
    with pd.option_context('display.max_colwidth', 100):
        print (grp)


## Listing the Most Active Departments Each Year 

for i in range(1998,2019):
    print("Departmental Breakdown in %d" % (i))
    print(full[full.year == i].groupby("DEPT_BY_CC")["froms"] \
                                .count() \
                                .reset_index(name='count') \
                                .sort_values(['count'], ascending=False))

## ------------------------------------------------------------------------------------ ##

## Summary of employees who have posted in memo-list
## Note: This is just a summary of people who have posted at least once in memo-list
    
people_count = full["froms"] \
                        .value_counts() \
                        .reset_index(name='count') \
                        .sort_values(['count'], ascending=False)
                        
x = people_count["count"]

print("--------------------------------------")
print("Summary Statistics")
print(x.describe())
print("--------------------------------------")
#print("Median")
#print(x.median())
#print("----------------------------------")
print("Number of People With over 1000 Posts")
print(x[x>1000].count())
print("--------------------------------------")
print("Number of People With over 100 Posts")
print(x[x>100].count())
print("--------------------------------------")
print("Number of People With over 25 Posts")
print(x[x>25].count())
print("--------------------------------------")
print("Number of People With 1 Post")
print(x[x==1].count())


