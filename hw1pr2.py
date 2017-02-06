#
# starter file for hw1pr2, cs35 spring 2017...
#

""" Wanted to answer three questions with my code:
    1. How often is each letter used as the starting letter of a word (weighted by frequency of word use)?
    2. What is the most common position for each letter in a word (weighted by frequency of word use)?
    3. What is the net positivity for every word starting with each letter (weighted by frequency of word use)?

CALL main() to see results!
"""

import csv
from collections import defaultdict
from textblob import TextBlob
from operator import itemgetter
import matplotlib.pyplot as plt


def main():
    """ This function calls the three helper functions to analyze the Project
        Gutenberg CSV file, creates a list of lists conatining the results,
        prints the results to another CSV called output, and returns a text formatted
        to create an html table
    """
    file = "wds.csv"
    starting_data = readcsv(file)                       # read in CSV file as list of lists
    letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    graph_range = range(1, 27)
    total_words = 0

    y_values_x_chart = []                               # these lists store the y values needed to represent analysis findings in pyplot charts
    y_values_y_chart = []
    y_values_z_chart = []

    x = weighted_first_letter_counter(starting_data)    # gets weighted frequency of each starting letter and puts them in a list of lists

    for letter in x:                                    # add the results from weighted frequency to appropriate list of y values
        y_values_x_chart.append(letter[1])
        total_words += letter[1]

    for letter in range(len(x)):                        # turn the results into a percentage to make it more intuitive
        y_values_x_chart[letter] = x[letter][1]/total_words

    f = plt.figure()                                    # create pyplot figure to rerpresent findings
    ax = f.add_axes([0.1, 0.1, .95, 0.8])
    ax.bar(graph_range, y_values_x_chart, align='center')
    ax.set_xticks(graph_range)
    ax.set_xticklabels(letter_list)
    ax.set_ylabel('Probability Word Starts With Letter Weighted by Usage')
    ax.set_xlabel('Letter')
    f.show()

    y = weighted_letter_place_predictor(starting_data)  # creates another LoL with most common position for each letter
    y_range = range(0, 5)

    for letter in y:                                    # add results to appropriate list of y values
        y_values_y_chart.append(letter[1][0])

    f1 = plt.figure()                                   # create pyplot chart
    ax = f1.add_axes([0.1, 0.1, 1, 0.8])
    ax.bar(graph_range, y_values_y_chart, align='center')
    ax.set_xticks(graph_range)
    ax.set_xticklabels(letter_list)
    ax.set_yticks(y_range)
    ax.set_ylabel('Most Common Index for Letter')
    ax.set_xlabel('Letter')
    f1.show()

    for letter in range(len(y)):                        # adds content from y in x's LoL; need everything in one list to put into csv file later
        x[letter].append(y[letter][1][0])

    z = start_sentiment(starting_data)                  # obtain sentiment for each letter

    for letter in z:
        y_values_z_chart.append(letter[1])

    f2 = plt.figure()                                   # create pyplot chart
    ax = f2.add_axes([0.1, 0.1, 1, 0.8])
    ax.bar(graph_range, y_values_z_chart, align='center')
    ax.set_xticks(graph_range)
    ax.set_xticklabels(letter_list)
    ax.set_ylabel('Net Sentiment for Words Starting with Letter')
    ax.set_xlabel('Letter')
    f2.show()

    for letter in range(len(z)):                        # add the sentiment data to x's LoL
        x[letter].append(z[letter][1])

    with open("output.csv", "w") as f:                  # writes the data from the .txt files to a CSV file
        writer = csv.writer(f)
        writer.writerows(x)

    final_html = csv_to_html('output.csv')
    print(final_html)


def weighted_first_letter_counter(data):
    """ This funciton returns the number of times each letter is used as the
        first letter in a word weighted by word frequency
    """
    first_letter_usage = defaultdict(int)      # tracks weight derived from word occurence
    frequency = defaultdict(int)               # tracks frequency of first letter

    for x in data:                             # iterate through every row in data to obtain frequencies
        first_letter = x[0][0]
        if first_letter.isalpha():
            first_letter = first_letter.lower()
            word_frequency = float(x[1])
            frequency[first_letter] += word_frequency
    freq = sorted(frequency.items())            # sort dictionary by items

    sorted_freq = []                            # need everything to come out sorted so I sort and round here

    for y in freq:                              # get everything out of a dictionary and into a list
        inner_list = []
        for z in y:
            inner_list.append(z)
        sorted_freq.append(inner_list)

    for x in sorted_freq:                       # round to 2 decimal places
        x[1] = "%.2f" % x[1]
        x[1] = float(x[1])
    return sorted_freq


def weighted_letter_place_predictor(data):
    """ This function returns where each letter is found most often weighted by frequency
    """
    letter_place = defaultdict(lambda: defaultdict(int))            # create a dictionary of dictionaries; store letters and all of the indexes that occur with appropriate weights

    for row in data:
        if row[0].isalpha():
            word = row[0].lower()
            freq = float(row[1])
            for letter in range(len(word)):
                letter_place[word[letter]][letter + 1] += freq

    sorted_letter_place = sorted(letter_place.items())              # have to make sure everything is sorted to blend all the lists together

    ig1 = itemgetter(1)                                             # get the modal index for each letter from nested dictionary
    maxes = {k: max((t for t in subdict.items()), key=ig1)
        for k, subdict in sorted_letter_place}

    # sorting results
    letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    output = []

    for letter in letter_list:
        output.append([letter, maxes[letter]])
    return output


def start_sentiment(data):
    """ Helper function that returns the net sentiment for every word
        beginning with a specific letter weighted by word frequency

        How happy are the words that start with the letter 'a' weighted
        by the frequency those words are used?
    """
    weighted_first_letter_sentiment = defaultdict(int)              # create a dictionary to store the data

    for row in data:                                                # go through the data, analyze every word's sentiment and add results to first letter
        if row[0].isalpha():
            word = row[0].lower()
            first_letter = word[0]
            frequency = float(row[1])
            word_for_analysis = TextBlob(word)                      # prep word for analysis
            sentiment_analysis = word_for_analysis.sentiment        # sentiment analysis
            word_sentiment = float(sentiment_analysis[0])           # get desired info from list returned
            weighted_sentiment = frequency*word_sentiment           # weight results by word usage
            weighted_first_letter_sentiment[first_letter] += weighted_sentiment

    letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    output = []

    for letter in letter_list:
        output.append([letter, weighted_first_letter_sentiment[letter]])        # sort results

    for x in output:                                                 # rounding results to 2 decimal places
        x[1] = "%.2f" % x[1]
        x[1] = float(x[1])

    return output


def readcsv(csv_file_name):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open(csv_file_name, newline='')  # open for reading
        csvrows = csv.reader(csvfile)              # creates a csvrows object

        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append(row)                  # adds only the word to our list

        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists

    except FileNotFoundError as e:
        print("File not found: ", e)
        return []


#
# write_to_csv shows how to write that format from a list of rows...
#  + try   write_to_csv( [['a', 1 ], ['b', 2]], "smallfile.csv" )
#
def write_to_csv(list_of_rows, filename):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open(filename, "w", newline='')
        filewriter = csv.writer(csvfile, delimiter=",")
        for row in list_of_rows:
            filewriter.writerow(row)
        csvfile.close()

    except:
        print("File", filename, "could not be opened for writing...")


#
# csv_to_html_table_starter
#
#   Shows off how to create an html-formatted string
#   Some newlines are added for human-readability...
#
def csv_to_html(csvfilename):
    """ csv_to_html_table_starter
           + an example of a function that returns an html-formatted string
        Run with
           + result = csv_to_html_table_starter( "example_chars.csv" )
        Then run
           + print(result)
        to see the string in a form easy to copy-and-paste...
    """
    data = readcsv(csvfilename)

    html_string = '<table>\n'    # start with the table tag

    for row in data:  # why is this saying I've got tuples in my data??
        html_string += '<tr> \n'
        for col in row:         # iterate over csv and add everything to html_string
            new_col = str(col)
            html_string += '<td>'
            html_string += new_col
            html_string += ' </td>'
            html_string += '\n'
        html_string += '</tr> \n'

    html_string += '</table>\n'
    return html_string
