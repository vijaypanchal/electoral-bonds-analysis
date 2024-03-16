import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

# Create a dictionary to store company objects
companies = {}
# Create a dictionary to store name to date to amount mapping
name_to_date_amount = {}
# Create a dictionary to store the total amount donated by each company
company_totals = {}


# Create a class to store company information
class Company:
    def __init__(self, name, date, amount):
        self.name = name
        self.date = date
        self.amount = amount


def read_load(infile, outfile):

    # Load the data from the Excel file
    data = pd.read_excel(infile)

    # Iterate row-wise through the data and store company information
    for index, row in data.iterrows():
        date = row['Date']
        name = row['Name']
        name = " ".join(name.split())
        amount = row['Amount']

        # Create a nested dictionary for date to amount mapping
        if name in name_to_date_amount:
            if date in name_to_date_amount[name]:
                name_to_date_amount[name][date] += amount
            else:
                name_to_date_amount[name][date] = amount
        else:
            name_to_date_amount[name] = {date: amount}

        # Create a new company object or update existing one
        if name in companies:
            companies[name].append(Company(name, date, amount))
        else:
            companies[name] = [Company(name, date, amount)]
    print("{:<60} {:<20}".format('Name', 'Total Amount'))
    # Print the stored company objects
    for name, company_info in companies.items():
        total_amount = 0

        for info in company_info:
            total_amount = total_amount + info.amount
            # print(f"Date: {info.date}, Amount: {info.amount}")
        # print(f"Name : {name}, Total Amount: {info.amount}")
        # print("{:<60} {:<20}".format(name, total_amount))
        company_totals[name] = total_amount

    # Sort the dictionary by total amount in descending order
    sorted_company_totals = dict(sorted(company_totals.items(), key=lambda x: x[1], reverse=True))

    for k in sorted_company_totals:
        print("{:<60} {:<20}".format(k, sorted_company_totals[k]))
    # Plot the companies and their total donation amounts
    plt.figure(figsize=(100, 100))
    plt.bar(sorted_company_totals.keys(), sorted_company_totals.values())
    plt.xlabel('Name')
    plt.ylabel('Amount')
    plt.title('Amount by Name')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig(outfile)


if __name__ == '__main__':

    if len(sys.argv) <= 2:
        print("No arguments were given Need Input Excel File")
        exit(1)
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    if os.path.exists(inputFile):
        read_load(inputFile, outputFile)
        exit(1)
    else:
        print("Error : ", inputFile, " File Not Exist!! ")
