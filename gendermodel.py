"""

Copyright (c) 2015 by Patrick Hall, jpatrickhall@gmail.com
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0
   
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

-------------------------------------------------------------------------------

This simple code is desinged to teach a basic user to read in the files in
python, simply find what proportion of males and females survived and make
a predictive model based on this.

Original Author: AstroDave
Date: 18 September 2012
Revised: 28 March 2014

"""
import csv
import numpy as np

# Load in the csv file
# Skip the fist line as it is a header
# Create a variable to hold the data
csv_file_object = csv.reader(open('train.csv', 'rb'))
header = csv_file_object.next()
data = []

# Skip through each row in the csv file,
# adding each row to the data variable
# Then convert from a list to an array.
for row in csv_file_object:
    data.append(row[0:])
data = np.array(data)

# Now I have an array of 12 columns and 891 rows
# I can access any element I want, so the entire first column would
# be data[0::,0].astype(np.float) -- This means all of the rows (from start to
# end), in column 0
# I have to add the .astype() command, because
# when appending the rows, python thought it was a string
# so needed to convert

# Set some variables
number_passengers = np.size(data[0::, 1].astype(np.float))
number_survived = np.sum(data[0::, 1].astype(np.float))
proportion_survivors = number_survived / number_passengers

# I can now find the stats of all the women on board,
# by making an array that lists True/False whether each row is female

# This finds where all the women are
women_only_stats = data[0::, 4] == "female"

# This finds where all the men are (note != means 'not equal')
men_only_stats = data[0::, 4] != "female"

# I can now filter the whole data, to find statistics for just women, by just
# placing women_only_stats as a "mask" on my full data -- Use it in place of
# the '0::' part of the array index. You can test it by placing it there, and
# requesting column index [4], and the output should all read 'female'
# e.g. try typing this: data[women_only_stats,4]
women_onboard = data[women_only_stats, 1].astype(np.float)
men_onboard = data[men_only_stats, 1].astype(np.float)

# and derive some statistics about them
proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

print 'Proportion of women who survived is %s' % proportion_women_survived
print 'Proportion of men who survived is %s' % proportion_men_survived

# Now that I have my indicator that women were much more likely to survive,
# I am done with the training set.
# Now I will read in the test file and write out my simplistic prediction:
# if female, then model that she survived (1)
# if male, then model that he did not survive (0)

# First, read in test.csv
test_file = open('test.csv', 'rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()

# Also open the a new file so I can write to it. Call it something descriptive
# Finally, loop through each row in the train file, and look in column index
# [3] (which is 'Sex'); Write out the PassengerId, and my prediction.

# Write the column headers
# for each row in test file,
# is it a female, if yes then
# write the PassengerId, and predict 1
# or else if male,
# write the PassengerId, and predict 0.
# Close out the files.
predictions_file = open("gendermodel.csv", "wb")
predictions_file_object = csv.writer(predictions_file)
predictions_file_object.writerow(["PassengerId", "Survived"])
for row in test_file_object:
    if row[3] == 'female':
        predictions_file_object.writerow([row[0], "1"])
    else:
        predictions_file_object.writerow([row[0], "0"])
test_file.close()
predictions_file.close()

