from Dates import cal_dates
from shortest_path import cal_path, dst
import pandas as pd
import pyfiglet

def rcmd_sftwr(grt = True, loc = True, tmp = True, directory = r'./1099005.csv'):
  df = pd.read_csv(directory)
  if grt == True:
    greet()

  if loc == True:
    print('\n\nWhat is the longitude and latitude to find the best path for your trip?')
    lon = get_inpt_num( -97.9851, -97.5678, str = 'longitude of the hotel you will be staying at in Austin, if possible to the 4th decimal,')
    lat = get_inpt_num( 30.1378, 30.5135, str = 'latitude of the hotel you will be staying at in Austin, if possible to the 4th decimal,')
    
    htl_loct = (lon, lat)
    path = cal_path(htl_loct)
    print('The best path to take from your hotel to your final destination, 6th Street, is (in order top to bottom):\n')
    for i in path:
      print(i)    

  if tmp == True:
    print('\n\n', 'What temperature would you like to have during your day trip? Keep in mind you will be walking outside alot.')
    
    temp = get_inpt_num( 50, 100, str = 'temperature, in Fareheit,')
    while len(cal_dates(df, temp)) == 0:
      print('There are no availible dates with that temperature, please choose a different temperature')
      temp = get_inpt_num( 50, 100, str = 'temperature, in Fareheit,')
    
    print('\n\nThe availible dates are:\n\n', cal_dates(df, temp))
  
  print('\nWould you like to go change your answers and run the software again?')
  again = get_yn()
  if again == False:
    return print('\nHave a safe trip, Goodbye.')
  
  else:    
    print('\nWould you like to change the location of the hotel?')
    loc = get_yn()
    
    print('\nWould you like to change the temperature would you like to have during your day trip?')
    tmp = get_yn()
    
    if loc == False and tmp == False:
      return print('\nHave a safe trip, goodbye.')
    
    rcmd_sftwr(grt = False, tmp=tmp, loc=loc)

def get_yn():
  while True:
    
    yn = input('\n Enter a y for yes or a n for no(in lowercase please):')
    if yn == 'y':
      return True
    
    elif yn == 'n':
      return False

def get_inpt_num( lwr_lmt, upr_lmt, str = 'number'):
  while True:
    
    var = input('\nInput '+str+f' that is in between {lwr_lmt} and {upr_lmt}: ')
    try:
      var = float(var)
      if lwr_lmt <= var <= upr_lmt:
        break
    
      print(f'The number must be bewteen {lwr_lmt} and {upr_lmt}.')
    
    except ValueError:
      print(f'Invalid answer! The number must be bewteen {lwr_lmt} and {upr_lmt}.')
      
  return var    

def get_temp():
  while True:
    
    temp = input('\nInput temperature you want that is in between 50 and 100: ')
    try:
      temp = int(temp)
      if 50 <= temp <= 100:
        break
    
      print('The number must be bewteen 50 and 100.')
    
    except ValueError:
      print('Invalid integer! The number must be bewteen 50 and 100.')
      
  return temp    

def greet():
  print(pyfiglet.figlet_format('WELCOME TO A PLANNED ONE DAY TRIP TO AUSTIN, TEXAS'))

  print('\n\n', 'This software reccommends a one day trip to Austin, Texas that is planned for you where we keep in mind the best temperature day for you. As you arrive from the airport, or driving, the planned trip starts off by unloading your luggage on your hotel. After unloading, the software calculates the best route between your hotel and the other locations you will be visiting. The locations you will visit first are: Camp Mabry or Great Hills. Then after visting both, during late afternoon, you will finish at 6th street where the night life is vibrant.' )
  return

rcmd_sftwr(grt = False)
