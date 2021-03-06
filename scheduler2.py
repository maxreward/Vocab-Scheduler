import argparse
import os
import sys
from datetime import datetime, timedelta

import pandas as pd

# 8 memory cycles (with the first three in the same day)
mem_cyc = [0, 1, 2, 4, 7, 15]


def get_unit_dates(start_date):
    """
    Returns the dates of memorizing a certain unit
    """
    global mem_cyc
    return [(start_date + timedelta(days=i)).strftime("%x") for i in mem_cyc]


def make_unit_view(num_units, start):
    """
    Make a unit view of the task
    """
    unit_view = {}
    for unit in range(num_units):
        unit_view[unit + 1] = get_unit_dates(start + timedelta(unit))
    return unit_view


def get_unique_dates(unit_view):
    """
    Returns all unique task dates
    """
    unique_dates = []
    for unit in unit_view.items():
        unique_dates += unit[1]
    return sorted(set(unique_dates))


def switch_date_view(unit_view, naming):
    """
    Switch to the date view
    """
    unique_dates = get_unique_dates(unit_view)
    ind_dates_pairs = []
    for index, dates in unit_view.items():
        for date in dates:
            ind_dates_pairs.append((index, dates.index(date) + 1, date))
    date_view_dict = {}
    for date in unique_dates:
        date_view_dict[date] = []
    for date in unique_dates:
        for pair in ind_dates_pairs:
            if pair[2] == date:
                date_view_dict[date].append(f"{naming[4]} {pair[0]} (Review {pair[1]})")
                ind_dates_pairs.remove(pair)
    date_view_dict = {
        k: v for k, v in sorted(date_view_dict.items(), key=lambda item: item[0][-2:])
    }
    for date, units in date_view_dict.items():
        units.sort(key=lambda x: x[-2])
        if len(units) == 6:
            continue
        elif units[0][-2] == "1" and len(units) < 6:
            date_view_dict[date] = units + ["N/A"] * (6 - len(units))
        elif units[0][-2] != "1" and len(units) < 6:
            date_view_dict[date] = ["N/A"] * (6 - len(units)) + units
    # print(date_view_dict)
    filename = f"date_view_{naming[0]}{naming[4].lower()}(s)_{naming[2]}_{naming[3]}_{naming[1]}"
    cols = [
        "Date",
        "Review 1 (three times)",
        "Review 2 (4th pass)",
        "Review 3 (5th pass)",
        "Review 4 (6th pass)",
        "Review 5 (7th pass)",
        "Review 6 (8th pass)",
    ]
    # Write to csv file
    with open(filename + ".csv", "w+") as file:
        for i in cols:
            file.write(f"{i}, ")
        file.write("\n")
        for date, units in date_view_dict.items():
            # units.sort(key=lambda x: x[-2])
            file.write(f"{date}, ")
            for unit in units:
                file.write(f"{unit}, ")
            file.write("\n")
    file.close()
    return date_view_dict


def main():
    parser = argparse.ArgumentParser(description="Vocab scheduler parser.")
    parser.add_argument("--units", default=None, type=int, required=True)
    parser.add_argument("--year", default=None, type=int, required=True)
    parser.add_argument("--month", default=None, type=int, required=True)
    parser.add_argument("--date", default=None, type=int, required=True)
    parser.add_argument("--name", default=None, type=str, required=True)
    args = parser.parse_args()
    # Prompts
    num_units = args.units
    start_date = datetime(args.year, args.month, args.date)
    naming = [args.units, args.year, args.month, args.date, args.name]
    # Make a dictionary of unit:dates pair
    unit_view = make_unit_view(num_units, start_date)
    # Make a dictionary of date:units pair
    date_view = switch_date_view(unit_view, naming)


if __name__ == "__main__":
    main()
