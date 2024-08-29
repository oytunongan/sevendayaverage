import csv
import requests


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")

    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


# TODO: Create a dictionary to store 14 most recent days of new cases by state
def calculate(reader):
    case_list = []
    _states = []
    sorted_states = []
    new_cases = {}
    for row in reader:
        _new_cases = {"state": row["state"], "date": row["date"], "cases": row["cases"]}
        case_list.append(_new_cases)
        _states.append(_new_cases["state"])

    sorted_states = sorted(set(_states))

    for i in range(len(sorted_states)):
        cases_prev = 0
        count = 0
        cases = []
        for line in sorted(case_list, key=lambda line: line["date"], reverse=True):
            if line["state"] in sorted_states[i] and count < 14:
                if (cases_prev - int(line["cases"]) > 0) or (cases_prev - int(line["cases"]) < 0):
                    cases_prev = int(line["cases"])
                    state = line["state"]
                    cases.append(cases_prev)
                    new_cases[state] = cases
                    count += 1
                else:
                    cases_prev = int(line["cases"])

    return new_cases


# TODO: Calculate and print out seven day average for given state
def comparative_averages(new_cases, states):
    for i in range(len(states)):
        sum_last = 0
        sum_first = 0
        ave_last = 0
        ave_first = 0
        for line in new_cases:
            if states[i] == line:
                sum_last = sum(new_cases[line][:7])
                sum_first = sum(new_cases[line][7:])
                ave_last = round(sum_last / 7)
                ave_first = round(sum_first / 7)
                while True:
                    try:
                        if ave_last > ave_first:
                            percent = round(((ave_last - ave_first) / ave_first) * 100)
                            print(f"{states[i]} had a 7-day average of {ave_last} and an increase of {percent}%")
                            break
                        elif ave_last < ave_first:
                            percent = round(((ave_first - ave_last) / ave_first) * 100)
                            print(f"{states[i]} had a 7-day average of {ave_last} and a decrease of {percent}%")
                            break
                    except ZeroDivisionError:
                        print("Zero division!")
                        break


main()
