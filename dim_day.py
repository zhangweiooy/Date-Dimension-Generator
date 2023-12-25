import pandas as pd
from lunar import Lunar
from chinese_calendar import is_holiday, is_workday


def getVacation(dateIds):
    vacationFlags = []
    i = 0
    while i < len(dateIds):
        ln = Lunar(dateIds[i])
        if ln.ln_date_str() == "农历腊月廿三":
            while Lunar(dateIds[i]).ln_date_str() != "农历正月十七":
                vacationFlags.append("Winter-vacation")
                i += 1
        if dateIds[i].month == 7 and dateIds[i].day == 1:
            while not (dateIds[i].month == 9 and dateIds[i].day == 1):
                vacationFlags.append("Summer-vacation")
                i += 1
        vacationFlags.append("Non-vacation")
        i += 1
    return vacationFlags


def getWeekday(i):
    n = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")
    return n[i]


def generateData(startDate="2019-1-01", endDate="2019-1-31"):
    d = {"id": pd.date_range(start=startDate, end=endDate)}
    data = pd.DataFrame(d)
    data["day_time"] = data["id"].apply(lambda x: x.strftime("%Y-%m-%d"))
    data["day_code"] = data["id"].apply(lambda x: x.strftime("%Y%m%d"))
    data["year"] = data["id"].apply(lambda x: x.year)
    data["quarter_number"] = data["id"].apply(lambda x: x.quarter)
    data["month"] = data["id"].apply(lambda x: "{:0>2}".format(x.month))
    data["day_number"] = data["id"].apply(lambda x: "{:0>2}".format(x.day))
    data["day_of_week"] = data["id"].apply(lambda x: getWeekday(x.dayofweek))
    data["week_of_year"] = data["id"].apply(
        lambda x: str(x.year + 1) + x.strftime("%V")
        if x.month == 12 and x.strftime("%V") == "01"
        else (
            str(x.year - 1) + x.strftime("%V")
            if x.month == 1 and x.strftime("%V") >= "50"
            else (str(x.year) + x.strftime("%V"))
        )
    )
    data["month_of_year"] = data["id"].apply(
        lambda x: str(x.year) + "{:0>2}".format(x.month)
    )
    data["weekend_flag"] = data["id"].apply(
        lambda x: "Weekend" if x.dayofweek == 5 or x.dayofweek == 6 else "Weekday"
    )
    data["holiday_flag"] = data["id"].apply(
        lambda x: "Non-holiday" if is_workday(x) else "Holiday"
    )
    data["vacation_flag"] = getVacation(data["id"])
    return data


data = generateData(startDate="2011-01-01", endDate="2023-12-31")
data.drop(columns=["id"], inplace=True)
data.to_csv("dim_day.csv", index=False, index_label=False)
