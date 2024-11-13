## Assignment 771768
#### Customer Data Pre-processing

### Background
You have been given a collection of data from a company wishing to process its customer records for business purposes **(acw_user_data.csv)**. The existing systems in-place at the company only export to a CSV file, and this is not in an appropriate format for analysis. You have been given the task of preparing this data for further analyses by your colleagues within the company, including representation changes, filtering, and deriving some new attributes / metrics for them.

These data include attributes such as first name, second name, credit card number, marital status, and even contains data on the customer’s car.
The number of records provided is significant, and therefore it is expected that solutions are robust to varying types of data, and varying values, offering a programmatic solution.

___

## Tasks
### Data Processing (70%)

Using standard python (No pandas / seaborn) with default libraries (os, sys, time, json, csv, …) you have been given the following tasks:
1. Read in the provided ACW Data using the CSV library.
2. As a CSV file is an entirely flat file structure, we need to convert our data back into its rich structure. Convert all flat structures into nested structures. These are notably:
    - Vehicle - consists of make, model, year, and type
    - Credit Card - consists of start date, end date, number, security code, and IBAN.
    - Address - consists of the main address, city, and postcode.
For this task, it may be worthwhile inspecting the CSV headers to see which data columns may correspond to these above.
Note: Ensure that the values read in are appropriately cast to their respective types.
3. The client informs you that they have had difficulty with errors in the dependants column. Some entries are empty (i.e. “ “ or “”), which may hinder your conversion from Task 2. These should be changed into something meaningful when encountered.
4. Print a list where all such error corrections take place. E.g. Problematic rows for dependants: [16, 58, 80, 98] Write all records to a processed.json file in the JSON data format. This should be a list of dictionaries, where each index of the list is a dictionary representing a singular person.
5. You should create two additional file outputs, retired.json and employed.json, these should contain all retired customers (as indicated by the retired field in the CSV), and all employed customers respectively (as indicated by the employer field in the CSV) and be in the JSON data format.
6. The client states that there may be some issues with credit card entries. Any customers that have more than 10 years between their start and end date need writing to a separate file, called remove_ccard.json, in the JSON data format. The client will manually deal with these later based on your output. They request that you write a function to help perform this, which accepts a single row from the CSV data, and outputs whether the row should be flagged. This can then be used when determining whether to write the current person to the remove_ccard file. Note the dates are shown in the format used on credit cards which is “MM/YY”.
7. You have been tasked with calculating some additional metrics which will be used for ranking customers. You should create a new data attribute for our customers called “Salary-Commute”. Reading in from processed.json:
   - Add, and calculate appropriately, this new attribute. It should represent the Salary that a customer earns, per Km of their commute. 
     - Note: If a person travels 1 or fewer commute Km, then their salary-commute would be just their salary.
   - Sort these records by that new metric, in ascending order.
   - Store the output file out as a JSON format, for a **commute.json** file.

___

### Data Visualisation (20%)
Your client wishes to understand the data they have on their customers a bit more by use of visualisations. With use of Pandas and Seaborn read in the original CSV file provided with the assignment.
1. Obtain the Data Series for Salary, and Age, and calculate the following:
   - Mean Salary 
   - Median Age
2. Perform uni variate plots of the following data attributes:
   - Age, calculating how many bins would be required for a bin_width of 5. 
   - Dependents, fixing data errors with seaborn itself. 
   - Age (of default bins), conditioned on Marital Status
3. Perform multivariate plots with the following data attributes:
   - Commuted distance against salary.
   - Age against Salary
   - Age against Salary conditioned by Dependants
4. Your client would like the ability to save the plots which you have produced. Provide a Notebook cell which can do this.
