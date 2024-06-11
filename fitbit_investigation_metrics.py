import matplotlib.pyplot as plt
import seaborn as sb
from scipy import stats
import pandas as pd
import numpy as np
from plotnine import *
import random

# Question 1a code

heart_rate_data = pd.read_csv("csv-metadata-full/heartrate_seconds_merged.csv")

heart_rate_data["Time"] = pd.to_datetime(heart_rate_data["Time"], format="%m/%d/%Y %I:%M:%S %p")

heart_rate_data["SecondsElapsed"] = (heart_rate_data["Time"] - heart_rate_data.groupby("Id")["Time"].transform("min")).dt.total_seconds()

unique_users = heart_rate_data["Id"].unique()[:5]

plt.figure(figsize=(12, 6))

for user_id in unique_users:
    user_data = heart_rate_data[heart_rate_data["Id"] == user_id][:25]
    plt.plot(user_data["SecondsElapsed"], user_data["Value"], label=f"User {user_id}")

plt.xlabel("Time Elapsed (Seconds)")
plt.ylabel("Heart Rate (BPM)")
plt.title("Heart Rate Timeline for Different FitBit Users")
plt.legend()

plt.show(observed=False)

# Question 1b code

sleep_data = pd.read_csv("csv-metadata-full/sleepDay_merged.csv")

sleep_data["Id"] = pd.Categorical(sleep_data["Id"])

average_sleep_durations = sleep_data.groupby("Id")["TotalMinutesAsleep"].mean().reset_index()

plot = (
    ggplot(average_sleep_durations, aes(x="Id", y="TotalMinutesAsleep"))
    + geom_bar(stat="identity", fill="lightblue")
    + labs(x="User ID", y="Average Tracked Sleep Duration (Mins)", title="Average Sleep Duration for FitBit Users")
    + theme(axis_text_x=element_text(rotation=90, hjust=0.5))
)

print(plot)

# Question 1c

step_data = pd.read_csv("csv-metadata-full/dailySteps_merged.csv")

step_data["Id"] = pd.Categorical(step_data["Id"])

average_daily_steps = step_data.groupby("Id")["StepTotal"].mean().reset_index()

step_plot = (
    ggplot(average_daily_steps, aes(x="Id", y = "StepTotal"))
    + geom_bar(stat="identity", fill="maroon")
    + labs(x="User Id", y="Average Daily Steps", title = "Average Daily Steps for FitBit Users")
    + theme(axis_text_x=element_text(rotation=90, hjust=.5))
)

print(step_plot)

# Question 1d code

weight_data = pd.read_csv("csv-metadata-full/weightLogInfo_merged.csv")
weight_data["Date"] = pd.to_datetime(weight_data["Date"])
most_values_id = weight_data["Id"].value_counts().idxmax()
useable_weight_data = weight_data[weight_data["Id"] == most_values_id]

weight_plot = (
    ggplot(useable_weight_data) + aes(x="Date", y="WeightPounds")
    + geom_point() + geom_line() + labs(x="Date", y="Weight in Pounds", title="Weight Change of FitBit User")
    + theme(axis_text=element_text(rotation=90, hjust=.5))
)
print(weight_plot)

hourly_cals = pd.read_csv("csv-metadata-full/hourlyCalories_merged.csv")
hourly_intensities = pd.read_csv("csv-metadata-full/hourlyIntensities_merged.csv")
hourly_steps = pd.read_csv("csv-metadata-full/hourlySteps_merged.csv")

all_hourly_dataframe = hourly_cals.merge(hourly_intensities, on=["Id", "ActivityHour"])
all_hourly_dataframe = all_hourly_dataframe.merge(hourly_steps, on=["Id", "ActivityHour"])

minute_cals_df = pd.read_csv("csv-metadata-full/minuteCaloriesNarrow_merged.csv")
minute_intensities_df = pd.read_csv("csv-metadata-full/minuteIntensitiesNarrow_merged.csv")
minute_METS_df = pd.read_csv("csv-metadata-full/minuteMETsNarrow_merged.csv")

all_minutes_dataframe = minute_cals_df.merge(minute_intensities_df, on=["Id", "ActivityMinute"])
all_minutes_dataframe = all_minutes_dataframe.merge(minute_METS_df, on=["Id", "ActivityMinute"])


daily_activity_df = pd.read_csv("csv-metadata-full/dailyActivity_merged.csv")
daily_sleep_df = pd.read_csv("csv-metadata-full/sleepDay_merged.csv")

daily_activity_df["Date"] = pd.to_datetime(daily_activity_df["ActivityDate"])
daily_sleep_df["Date"] = pd.to_datetime(daily_sleep_df["SleepDay"])
all_hourly_dataframe["Date"] = pd.to_datetime(all_hourly_dataframe["ActivityHour"])
all_minutes_dataframe["Date"] = pd.to_datetime(all_minutes_dataframe["ActivityMinute"])

print(daily_activity_df.head(5))





#Question 2.3 code

heartrate_seconds_df = pd.read_csv("csv-metadata-full/heartrate_seconds_merged.csv")
heartrate_per_min = heartrate_seconds_df.groupby(heartrate_seconds_df.index // 12).agg(
    Id=("Id", "first"),
    Average_Rate=("Value", "mean")
).reset_index(drop=True)
print(heartrate_per_min.head(10))



daily_steps_df = pd.read_csv("csv-metadata-full/dailySteps_merged.csv")
daily_cals_df = pd.read_csv("csv-metadata-full/dailyCalories_merged.csv")
daily_intensity_df = pd.read_csv("csv-metadata-full/dailyIntensities_merged.csv")
hourly_intensity_df = pd.read_csv("csv-metadata-full/hourlyIntensities_merged.csv")
hourly_cals_df = pd.read_csv("csv-metadata-full/hourlyCalories_merged.csv")

daily_steps_and_cals_df = daily_steps_df.merge(daily_cals_df, on=["Id", "ActivityDay"])
daily_steps_and_cals_df = daily_steps_and_cals_df[daily_steps_and_cals_df.StepTotal != 0]
steps_vs_cals = (
    ggplot(daily_steps_and_cals_df.sample(500)) + aes(x="StepTotal", y="Calories")
    + geom_point() + geom_smooth(method="lm", se=False) + labs(x="Step Count", y="Calories Burned", title="Step Count v Calories Burned")
)

print(steps_vs_cals)

hourly_intensity_and_cals_df = hourly_cals_df.merge(hourly_intensity_df, on=["Id", "ActivityHour"])
hourly_intensity_and_cals_df = hourly_intensity_and_cals_df[hourly_intensity_and_cals_df["AverageIntensity"] != 0]
intensity_vs_cals = (
    ggplot(hourly_intensity_and_cals_df.sample(500)) + aes(x="AverageIntensity", y="Calories")
    + geom_point() + geom_smooth(method="lm", se=False) + labs(x="Average Intensity of Workout", y="Calories Burned", title="Intensity vs Calories Burned")
)

print(intensity_vs_cals)


sleep_df = pd.read_csv("csv-metadata-full/sleepDay_merged.csv")

in_bed_vs_sleep = (
    ggplot(sleep_df) + aes(x="TotalTimeInBed", y="TotalMinutesAsleep")
    + geom_point() + geom_smooth(method="lm", se=False) + labs(x="Total Time Spent in Bed (Mins)", y= "Total Time Actually Asleep (Mins)", title="Time in Bed vs Time Asleep")
)

print(in_bed_vs_sleep)


# Question 3.3 Code

hourly_intensity_df["ActivityHour"] = pd.to_datetime(hourly_intensity_df["ActivityHour"])
hourly_intensity_df["Hour"] = hourly_intensity_df["ActivityHour"].dt.hour

unique_ids = hourly_intensity_df["Id"].unique()
sampled_Ids = random.sample(list(unique_ids), 5)

hourly_intensity_df_filtered = hourly_intensity_df[hourly_intensity_df["Id"].isin(sampled_Ids)]
hourly_intensity_df_filtered["Id"] = hourly_intensity_df_filtered["Id"].astype(str)
mean_intensity_data = hourly_intensity_df_filtered.groupby(['Id', 'Hour'])['AverageIntensity'].mean().reset_index()

intensity_throughout_day = (
    ggplot(mean_intensity_data) + aes(x="Hour", y="AverageIntensity", fill="Id") +
    geom_bar(stat="identity", position="dodge", width=.8) + labs(x="Hour of the Day", y="Average Intensity", title="Intensity over the Day") +
    scale_fill_discrete(name="Id")
)

intensity_throughout_day += theme(figure_size=(12,6))

print(intensity_throughout_day)


# Question 3.4 Code

sedentary_df = pd.read_csv("csv-metadata-full/dailyIntensities_merged.csv")
sleep_df = pd.read_csv("csv-metadata-full/sleepDay_merged.csv")

sedentary_df['ActivityDay'] = pd.to_datetime(sedentary_df['ActivityDay'])
sleep_df['SleepDay'] = pd.to_datetime(sleep_df['SleepDay'])

sleep_sedentary_df = sedentary_df.merge(sleep_df, left_on=['Id', 'ActivityDay'], right_on=['Id', 'SleepDay'], how='inner')
sleep_sedentary_df = sleep_sedentary_df[["Id", "ActivityDay", "TotalMinutesAsleep", "SedentaryMinutes"]]

sleep_vs_sedentary_plot = (
    ggplot(sleep_sedentary_df) + aes(x="SedentaryMinutes", y="TotalMinutesAsleep") + geom_point()
    + geom_smooth(method='lm', se=False) + labs(x="Total Minutes Sedentary", y="Total Minutes Asleep", title="Time Spent Sedentary vs Time Spent Sleeping")
)

print(sleep_vs_sedentary_plot)


# Two variables that have most / least differences for Calories

# Choice 1: Daily Steps and Calories

'''
H0: There is no difference in the average amount of calories burned when users have
over 10k steps eclipsed compared to when they do not eclipse 10k steps

Ha: There is a difference in the average amount of calories burned when users have 
over 10k steps eclipsed
'''

alpha = .05

cal_data = pd.read_csv("csv-metadata-full/dailyCalories_merged.csv")
step_data = pd.read_csv("csv-metadata-full/dailySteps_merged.csv")

steps_and_cals = cal_data.merge(step_data, on=["Id", "ActivityDay"])
ten_and_under_df = steps_and_cals[steps_and_cals["StepTotal"] <= 10000]
over_ten_df = steps_and_cals[steps_and_cals["StepTotal"] > 10000]

new_df = ten_and_under_df.groupby("Id")["Calories"].mean().reset_index()
new_df = new_df.rename(columns={"Calories": "CaloriesBurnedUnderTen"})
over_new_df = over_ten_df.groupby("Id")["Calories"].mean().reset_index()
over_new_df = over_new_df.rename(columns={"Calories": "CaloriesBurnedOverTen"})

testing_df = new_df.merge(over_new_df, on="Id")

t_statistic, p_value = stats.ttest_rel(testing_df["CaloriesBurnedUnderTen"], testing_df["CaloriesBurnedOverTen"])
print(p_value)

# The p-value is less than our alpha(0.5), so we reject the H0.


# Choice 2: Calories and Minutes Asleep

'''
H0: There is no difference in the average amount of daily calories burned when users
get 8 hours or more of sleep compared to less than 8 hours

Ha: There is a difference in the average amount of daily calories burned when users get 8 hours or more
of sleep compared to less than 8 hours
'''

alpha = .05
cals_df = pd.read_csv("csv-metadata-full/dailyCalories_merged.csv")
sleep_df = pd.read_csv("csv-metadata-full/sleepDay_merged.csv")
cals_df["ActivityDay"] = pd.to_datetime(cals_df["ActivityDay"])
sleep_df["SleepDay"] = pd.to_datetime(sleep_df["SleepDay"])

sleep_and_cals = cals_df.merge(sleep_df, left_on=["Id", "ActivityDay"], right_on=["Id", "SleepDay"])
sleep_and_cals = sleep_and_cals[["Id", "ActivityDay", "Calories", "TotalMinutesAsleep"]]

under_sleep_df = sleep_and_cals[sleep_and_cals["TotalMinutesAsleep"] < 480]
over_sleep_df = sleep_and_cals[sleep_and_cals["TotalMinutesAsleep"] >= 480]

under_new_df = under_sleep_df.groupby("Id")["Calories"].mean().reset_index()
under_new_df = under_new_df.rename(columns={"Calories": "LowSleepCals"})
over_new_df = over_sleep_df.groupby("Id")["Calories"].mean().reset_index()
over_new_df = over_new_df.rename(columns={"Calories": "GoodSleepCals"})

final_merged_df = under_new_df.merge(over_new_df, on="Id")

t_statistic, p_value_2 = stats.ttest_rel(final_merged_df["LowSleepCals"], final_merged_df["GoodSleepCals"])
print(p_value_2)

# Our p-value is greater than out alpha(.05) so we fail to reject H0