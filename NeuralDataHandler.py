import csv


def load_data(directory='Neural_Net_Chart.csv'):
    # output format is list: [ Ace?(1/0), Sum(Player), Sum(Dealer), Result (S/H/D) ]
    with open(directory) as chart:
        csv_reader = csv.reader(chart, delimiter=",")
        output_list = list()
        # the [1:] skips the first element value
        for row in csv_reader:
            i = 1
            for col in row[1:]:
                i += 1
                # if its the first row, detect the value for this
                if row[0] == '0':
                    break
                print(row, " ", col)
                # if the hand value has no Ace
                if row[0].find("A") == -1:
                    output_list.append([0, row[0], i, col])
                else:
                    ace_sum = handle_ace_sum(row[0].split(","))
                    output_list.append([1, ace_sum, i, col])
        return output_list


def handle_ace_sum(hand_list):
    # if the card is an ace we must have a special condition for it
    # An ace is considered a one when returned, the calculation determines if it can be an 11
    # Consider an Ace as 11 unless that brings you over (eg. 2 aces)
    if hand_list[0] == "A" and hand_list[1] == "A":
        return "12"
    elif hand_list[0] == "A":
        return str(11 + int(hand_list[1]))

val = load_data()
print(val)
