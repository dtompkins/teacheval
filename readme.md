     _                  _                     _ 
    | |                | |                   | |
    | |_ ___  __ _  ___| |__   _____   ____ _| |
    | __/ _ \/ _` |/ __| '_ \ / _ \ \ / / _` | |
    | ||  __/ (_| | (__| | | |  __/\ V / (_| | |
     \__\___|\__,_|\___|_| |_|\___| \_/ \__,_|_|

[https://github.com/dtompkins/teacheval]
by Dave Tompkins [http://dtompkins.com]
 
This repository is part of my ongoing commitment to improve my teaching and to be open and transparent about my teaching.

It contains:

1) The raw data for ALL of the evaluations (good and bad) that I have received from my students, including their individual comments.

2) The python scripts to take that raw data, along with some template files, and automatically generate the pretty pages located at: https://cs.uwaterloo.ca/~dtompkin/teaching/

3) The source files for generating the 'random' evaluation page


A brief description of how to use the data:

For each section, there is a data/section-id.csv file.  It contains:

* the course-id:
  * the templates/course-id.csv file stores additional course information
* the template-id:  
  * the templates/template-id.csv has all of the question information
  * the templates/template-id.html has all of the layout information
* additional information (e.g., term, section number) to display  

There is also (likely) a data/section-id-responses.csv file:
* The first row (header) has the question id for each column:
  * mc: multiple choice
  * txt: text response
  * smc: summarized multiple choice (see note below)
* Each subsequent row has a single student's response
  
There may also be a data/section-id-comments.txt file containing my personal comments on the section.


SMC (Summarized Multiple Choice):
* The first data row (after the header) has the number of possible choices per question
* Each subsequent row contains the number of students that selected the corresponding choice.
