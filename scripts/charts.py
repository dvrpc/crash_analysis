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

def pie_chart(df):
    """
    Creates a pie chart for injuries and fatalities versus total crashes in the study area
    """
    year=df["crash_year"].median() #placeholder until year is a variable in the main function
    total_crashes = len(df.index)
    injury_count= df["maj_inj_count"].sum()
    fatality_count=df["fatal_count"].sum()
    total_minus_fatal_and_inj = (total_crashes-injury_count-fatality_count)
    data = [injury_count,fatality_count,total_minus_fatal_and_inj]
    labels = ["Injuries", "Fatalities", "Other Crashes"]
    plt.title(f'{total_crashes} Crashes in Study Area in {round(year)}')
    plt.pie(x=data, labels=labels, autopct= lambda x: '{:.0f}'.format(x*sum(data)/100))
    plt.savefig(f'{ev.DATA_ROOT}/injury_fatality_piechart.png')



if __name__ == "__main__":
    pie_chart(df)