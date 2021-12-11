import csv
males = 0
above_threshold = 0
hr = 0

gender_index = 4
age_index = 5
department_index = 6

male_text = 'Male'
age_threshold = 30
hr_department_name = 'Human Resources'

# function to process csv file to retrieved information needed
def process(raw_csv_data):
  # redeclaring of global variables in order to access them in function 
  # and increment their counter when needed
  global males
  global above_threshold
  global hr

  #converting the raw file data into a more manageable format, and removed header
  csvreader = csv.reader(raw_csv_data)
  next(csvreader) 

  #reset global variables
  males = 0
  above_threshold = 0
  hr = 0

  #looping through each row of the csv file, in order to retrieve information needed
  for row in csvreader:
    males = calculate_males(row)
    above_threshold = calculate_above_threshold(row)
    hr = calculate_hr(row)

  # built an object that will return the information retrieved
  result = {"males": males, "above_threshold": above_threshold, "hr": hr}
  return result

def calculate_males(row) :
  return males + 1 if male_text == row[gender_index] else males

def calculate_above_threshold(row) :
    return above_threshold + 1 if age_threshold <= int(row[age_index]) else above_threshold

def calculate_hr(row) :
  return hr + 1 if hr_department_name == row[department_index] else hr
