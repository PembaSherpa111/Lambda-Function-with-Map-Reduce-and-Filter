import csv
import json
from functools import reduce

#function to calculate average 
def AVG(police_report,variable):
    total_time_report = filter(lambda report: report[variable] != '', police_report) 
    total_time_report  = list(total_time_report )

    total_time = [] 
    for i in range(0,len(total_time_report )):
        total_time.append(float((total_time_report [i])[variable]))

    sum_total_time = reduce(lambda total_time1, total_time2: total_time1 + total_time2, total_time) 
    avg_total_time = sum_total_time/len(total_time)
    return avg_total_time

#function to calculate average by neighborhood
def AVG_neighborhood(neighborhood,neighborhood_report,variable):
    avg_time_neighborhood = []
    for i in range(0,len(neighborhood_report)):
        avg = AVG(neighborhood_report[i],variable)
        neighborhood_name = neighborhood[i]
        avg_time_neighborhood.append({neighborhood_name:avg})
    return avg_time_neighborhood

#Main 
with open('911_Calls_for_Service_(Last_30_Days).csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader_list = list(reader) #converitng csv.reader file to list

#creating a list of dictionary
key = reader_list[0] #header
police_report=[] #empty list to append the dictionary

for i in range(1,len(reader_list)):
    value = reader_list[i]
    dictionary = {k:v for k,v in zip(key,value)} #forming key:value pair between list of header and list of value
    police_report.append(dictionary)

#removing the dictionary which has missing data in the Zip, or Neighborhood columns
police_report = filter(lambda police_report: police_report['zip_code'] != '0' or police_report['neighborhood'] != '', police_report)
police_report = list(police_report)

#calculate the average total response time
avg_total_response_time = AVG(police_report,'totalresponsetime')
print(f'Average total response time: {avg_total_response_time}')

#calculate the average total dispatch time
avg_total_dispatch_time = AVG(police_report,'dispatchtime')
print(f'Average total dispatch time: {avg_total_dispatch_time}')

#calculate the average total time
avg_total_time = AVG(police_report,'totaltime')
print(f'Average total time: {avg_total_time}')

#divide the list of dictionaries into smaller lists of dictionaries separated by neighborhood.
neighborhood = [] #creating just the unique list of neighborhood
for i in range(0,len(police_report )):
    if (police_report [i])['neighborhood'] not in neighborhood:
        neighborhood.append((police_report [i])['neighborhood'])

neighborhood_report = []
for i in range(0,len(neighborhood)): #creating list of dictionaries by neighborhood
    neighborhood_name = neighborhood[i]
    report_by_neighborhood = filter(lambda report: report['neighborhood'] == neighborhood_name, police_report )
    report_by_neighborhood = list(report_by_neighborhood)
    neighborhood_report.append(report_by_neighborhood)

#find the average total response time for each neighborhood
avg_totalresponsetime_neighborhood = AVG_neighborhood(neighborhood, neighborhood_report,'totalresponsetime')

#find  the average dispatch time for each neighborhood
avg_dispatchtime_neighborhood = AVG_neighborhood(neighborhood, neighborhood_report,'dispatchtime')

#find the average total time for each neighborhood 
avg_totaltime_neighborhood = AVG_neighborhood(neighborhood, neighborhood_report,'totaltime')

with open("neighborhood_report.json","w") as writer:
    json.dump(neighborhood_report,writer)

with open("avg_totalresponsetime_neighborhood.json","w") as writer:
    json.dump(avg_totalresponsetime_neighborhood,writer)

with open("avg_dispatchtime_neighborhood.json","w") as writer:
    json.dump(avg_dispatchtime_neighborhood,writer)

with open("avg_totaltime_neighborhood.json","w") as writer:
    json.dump(avg_totaltime_neighborhood,writer)