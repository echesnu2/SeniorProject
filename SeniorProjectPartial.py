
from datetime import date
import calendar

@app.route('/calender')
def calender():
    d = date.today()
    start_date = date(d.year, d.month, 1).weekday() + 1
    month = calendar.month_name[d.month]
    m_range = calendar.monthrange(d.year, d.month)
    end_date = m_range[1]

    ## Need to create a dictionary with the key being the day of the month its on as an integer
    ## Value can be string or array to handle on front end
    activities = {4: 'Soccer: 7:30', 21: 'Baseball - 6:30', 15: 'Chess Match', 2: 'Free Running'}
    keys = list(activities.keys())
    print(keys)

    return render_template('calender.html', user=' ', activity=activities, keys=keys,
                           current=d.day, start=start_date, date=d, month=month, end_date=end_date)
