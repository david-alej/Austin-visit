import pandas as pd

# df = pd.read_csv(r'./1099005.csv')

def comb(temp_array, temp, temp_range, start):
  for i in range(len(temp_array)):
    if temp_array[i] in range(int(temp - temp_range), int(temp + temp_range)):
      temp_array[i] = temp
      
    else:
      temp_array[i] = i+start
  return temp_array

def common_temp(a,b,c):
  l = []
  for i in range(len(a)):
    if a[i] == b[i] == c[i]:
      l.append(i)
  
  return l

def common_dates(data_frame, idx_list):
  l1 = []
  for i in idx_list:
    l1.append(data_frame.DATE[data_frame.index[0]+i])
  return l1

def cal_dates(df, temp=70, temp_range = 5):
  #getting all the different location names:
  # Airport, Camp Mabry, 6th Street, Great Hills
  names = []
  diffname= ''
  for i in df.NAME:
    if i != diffname:
      names.append(i)
      diffname = i
  
  # Storing data of average temperature in temp_avg
  # by taking using Max temperatuer and Min temperature.
  # Then move data in data frame to a different lists 
  # for different locations inside a dictionary.
  tmp_avg = (df.TMAX + df.TMIN)/2
  name_keys = {}
  start = 0
  for i in names:
    for j in range(len(df.NAME[start:])):
      if i != df.NAME[j+start]:
        end = j+start
        break
      elif j == len(df.NAME[start:])-1 and names[-1] == df.NAME[len(df.NAME[:])-1]:
        end = len(df.NAME[:])
        break
  
    name_keys[i] = [k for k in tmp_avg.copy()[start:end]]
    # Editing name_keys's keys so that they loose fluf on
    # the string.
    name_keys[i.replace("AUSTIN ", "").replace(", TX US", "")] = name_keys.pop(i)
    start = end
  
  # remvoing fluff for lists too.
  names = [i.replace("AUSTIN ", "").replace(", TX US", "") for i in names]
  
  # Since we are going from the airport to check in to
  # the hotel we wont be spending time outside so temperature
  # Doesnt matter. So we eliminate airport which is our
  # first element in our dictionary and list.
  name_keys.pop(names[0])
  del names[0]
  
  # Re-adjusting ourthe lengths of our lists inside
  # the dictionaries so that they are all equal. We note
  # that each lost begins on the same day but some have
  # longer surveys of temperatures.
  length = min(len(name_keys[names[0]]), 
               len(name_keys[names[1]]),
               len(name_keys[names[2]]))
  
  
  name_keys[names[0]] = name_keys[names[0]][0:length]
  name_keys[names[1]] = name_keys[names[1]][0:length]
  name_keys[names[2]] = name_keys[names[2]][0:length]
  
  start = 100
  for i in names:
    name_keys[i] = comb(name_keys[i], temp, temp_range, start)
    start += 500
    
  # Then we plug into a function that finds the list
  # of indices that have the acceptable average temp on
  # all 3 locations.
  cmn_tmp = common_temp(name_keys[names[0]], 
                        name_keys[names[1]],
                        name_keys[names[2]])
  
  # Finally we finish by calling afunction that will
  # return all days that are within the average temp
  # of the temperature range.
  return common_dates(df, cmn_tmp)
   

##OLD COLD Below and my thinking process
#______________________________________________________
# ______________________________________________________
# _____________________________________________________
# df = pd.read_csv(r'~/Learning Python/.venv/Recommendation Software/1099005.csv')
#print(df.shape, df)

# We at most will use columns, starting counting with 0, NAME, Date, TAVG, TMax, and TMIn. Also, that looking at the full csv file we see 4 different locations/Names, so we have to find what rows each name occupies.
# print(df.columns, df.NAME[0])

# for i in range(len(df.NAME)):
#   end1 = 0
#   if end1 == False and df.NAME[i] != df.NAME[0]:
#     end1 = i
#     break
  
# for i in range(end1, len(df.NAME)):
#   end2 = 0
#   if end2 == False and df.NAME[i] != df.NAME[end1]:
#     end2 = i
#     break

# for i in range(end2, len(df.NAME)):
#   end3 = 0
#   if end3 == False and df.NAME[i] != df.NAME[end2]:
#     end3 = i
#     break
#We then have then have each locations at rows:
#Airport (air)  [0,end1 - 1]
#Museum (mus) [end1,end2 -1]
#West Strip (stp) [end2,end3]
#Shopping Center (shp) [end3, ]

# air = df[0:end1]
# mus = df[end1:end2]
# stp = df[end2:end3]
# shp = df[end3:]

#Looking at the data we see each measurement of each temp dates from 
#2016-7-11 to at least 2017-10-11. We also see locations for a certain 
# amount of days over:

#Airport : 2 days 
#Mabry : 0 days
#Great Hills : 1 days
#6th Street : 2 days

#We see that coresponding to temperature the airport is irrelevant since 
#you can mostly stay inside and when being at the other locations you are
#walikng outside. So we try to find the longest common days that are next to
#each other by usinga modification to the longest common subsequence.
#Trying to eliminate days so that each string can share the came amount
#of days.

# stp = stp[0:len(stp)-2]
# shp = shp[0:len(shp)-1]

#Next we comb our data so it is ready for us to compare
#the dates to find the longest series of days that have
#good temperature.
#Calculating the temperature of the day by taking average between the 
#minimum temp and maximum temp for each locaiton.
#Temp_range referse to range of temperature that you want
#to on the trip. Can eithere be 60, 70, 80 and is an
#integer.
# def comb(temp_array, temp_range, start):
#   for i in range(len(temp_array)):
#     if temp_array[i] in range(temp_range, temp_range+10):
#       temp_array[i] = temp_range + 5
      
#     else:
#       temp_array[i] = i+start
#   return temp_array

# temp_range = 70     
# mus_temp = comb(mus, temp_range, 100)
# stp_temp = comb(stp, temp_range, 700)
# shp_temp = comb(shp, temp_range, 1300)

# Then we find the list of indices where the 3 lists have
# the same temperature on the same day.
# def common_temp(a,b,c):
#   l = []
#   for i in range(len(a)):
#     if a[i] == b[i] == c[i]:
#       l.append(i)
  
#   return l

# cmn_tmp = common_temp(mus_temp,
#                   stp_temp,
#                   shp_temp)
# print(cmn_tmp)

# def common_dates(data_frame, idx_list):
#   l1 = []
#   for i in idx_list:
#     l1.append(data_frame.DATE[data_frame.index[0]+i])
#   return l1
    
# print(common_dates(shp, cmn_tmp))
# def p(a,b,c,start, end=False):
#   if end == False:
#     return print(a[start], b[start], c[start])  
#   else:
#     return print(a[start:end], b[start:end], c[start:end])
  
# p(mus_temp,shp_temp,stp_temp, 255)