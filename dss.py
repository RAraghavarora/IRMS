# Null Hypothesis H0: 𝞵1⩽ 𝞵0
# Alternate Hypothesis 𝞵1 > 𝞵0
# Confidence Interval: 95%
# ❲𝒙-𝞵o❳/𝝈/√n⩽ 1.96: Accept null hypothesis
# ❲𝒙-𝞵o❳/𝝈/√n＞1.96: Reject null hypothesis
# For the years 2014-2018

from portal.models import Biblio, Items

issues = []
item_count=[0]
issue_count = [0]
data = []
sample_mean_dict = {}
counter = 0

issue_instances = []

biblio_list = Biblio.objects.all()

for biblio in biblio_list:
    items = biblio.items_set.all() # All the items of the biblio
    book_issues = [] # To store the number of issues of each item of the biblio
    book_item_count = [0] # Total number of items with the appropriate itemtype for the biblio
    for item in items:
        yearwise_issues = [0]*5
        # List of all yearwise issues of a book
        if item.itype in ('R', 'SPR', 'STB', 'DIVB', 'C'):
            book_item_count[0]+=1
            item_count[0]+=1
            issue = [0]
            try:
                iss = item.issue
                # Find the index number for yearwise_issues from the last digit of issuedate.year If year is 2018, index=8-4 = 4
                index = iss.issuedate.year%10 - 4
                if index in range(0,5):
                    yearwise_issues[index]+=1
                if iss.issuedate.year in (2014,2015,2016,2017,2018):
                    issue_instances.append(iss)
                    issue[0]+=1
            except IndexError:
                print(index)
                raise Exception('Invalid Index debug')
            except Items.issue.RelatedObjectDoesNotExist:
                # No issue exists
                pass
            count=[0,0]
            for old_issue in item.oldissues_set.all():
                if old_issue.issuedate.year in (2014,2015,2016,2017,2018):
                    count[0]+=1
                    issue[0]+=1
                    issue_instances.append(old_issue)
                index = old_issue.issuedate.year%10 - 4
                if index in range(0,5):
                    yearwise_issues[index]+=1
                    count[1]+=1
            assert count[0] == count[1], "Check why"
            data += yearwise_issues
            issue_count[0] += issue[0]
            book_issues.append(issue[0])
        else:
            continue
    if book_item_count[0]>0:
        sample_mean = sum(book_issues) / (book_item_count[0]*5)
        sample_mean_dict[biblio.biblionumber] = sample_mean
    issues.append(book_issues)
    print(counter)
    counter+=1


import statistics
from math import sqrt

population_mean = statistics.mean(data)
variance = statistics.variance(data)
sigma = statistics.stdev(data)
N = len(data)

stdev = sigma/sqrt(N)
rejected = {}
accepted = {}

for biblionumber,sample_mean in sample_mean_dict.items():
    z_calc = (sample_mean - population_mean)/(stdev)
    if z_calc > 1.96:
        rejected[biblionumber] = z_calc
    else:
        accepted[biblionumber] = z_calc









print(item_count[0])
lengths = list( map (lambda book_list: len(book_list) , issues))
N = sum(lengths)
print(N)
assert N==item_count[0], 'Total Item count error'

sums = list( map( lambda issue_list: sum(issue_list), issues ) )
assert issue_count[0]==sum(sums), "Total number of issues count error"

print(sum(data))
print(len(data))
print(raghav)

print("Successful")

import math
sigma = stdev/math.sqrt(N)












rejected = []
fail_to_reject = []
just=[0]
for biblio in Biblio.objects.all():
    items = biblio.items_set.all()
    book_issue_count = [0]
    book_item_count = [0]
    for item in items:
        if item.itype in ('R', 'SPR', 'STB', 'DIVB', 'C'):
            book_item_count[0]+=1
            try:
                iss = item.issue
                if iss.issuedate.year in (2014,2015,2016,2017):
                    book_issue_count[0]+=1
                else:
                    pass
            except:
                pass
            for oldissue in item.oldissues_set.all():
                if oldissue.issuedate.year in (2014,2015,2016,2017):
                    book_issue_count[0]+=1
                else:
                    pass
    if book_item_count[0]>0:
        sample_mean = book_issue_count[0] / ((book_item_count[0])*5)
        z_calc = (sample_mean - mean)/sigma
        if z_calc>1.96:
            # Reject Null hypothesis ---> Buy new copy of the book
            rejected.append(biblio)
        else:
            fail_to_reject.append(biblio)
    print(just[0])
    just[0]+=1
