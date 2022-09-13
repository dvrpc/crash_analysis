"""
charts.py
------------------
This script runs the main function from data_setup.py and parses the results into charts, which are 
then saved to the project directory.

"""
import matplotlib.pyplot as plt
from data_setup import clip_crashes
import env_vars as ev

df = clip_crashes()
year=df["crash_year"].median() #placeholder until year is a variable in the main function
total_crashes = len(df.index)
injury_count= df["maj_inj_count"].sum()
fatality_count=df["fatal_count"].sum()
ped_count=df["ped_count"].sum()
bicycle_count=df["bicycle_count"].sum()
total_minus_fatal_and_inj = (total_crashes-injury_count-fatality_count)
total_minus_bike_ped_count = (total_crashes-ped_count-bicycle_count)


def injury_pie_chart(df):
    """
    Creates a pie chart for injuries and fatalities versus total crashes in the study area
    """
    data = [injury_count,fatality_count,total_minus_fatal_and_inj]
    labels = ["Injuries", "Fatalities", "Other Crashes"]
    plt.title(f'{total_crashes} Crashes in Study Area in {round(year)}')
    plt.pie(x=data, labels=labels, autopct= lambda x: '{:.0f}'.format(x*sum(data)/100))
    plt.savefig(f'{ev.DATA_ROOT}/injury_fatality_piechart.png')
    plt.cla()

def mode_pie_chart(df):
    """
    Creates a pie chart for breakdown of crashes by mode
    """
    data= [ped_count,bicycle_count,total_minus_bike_ped_count]
    mode_labels = ["Pedestrian", "Cyclist", "Vehicular Crashes"]
    plt.title(f'{total_crashes} Crashes in Study Area in {round(year)}')
    plt.pie(x=data, labels=mode_labels, autopct= lambda x: '{:.0f}'.format(x*sum(data)/100))
    plt.savefig(f'{ev.DATA_ROOT}/mode_piechart.png')
    plt.cla()


if __name__ == "__main__":
    print("Generating charts.. See project directory for images...")
    injury_pie_chart(df)
    mode_pie_chart(df)