import requests
import matplotlib.dates as mdates 
import smtplib as smlib 
import json 
import matplotlib.pyplot as plt 
import matplotlib as mpl 
import keyring as kr # Password safety
import os  
from datetime import datetime 
from matplotlib import cm
from http import HTTPStatus
from email.message import EmailMessage 
from dotenv import load_dotenv

load_dotenv() # Access .env-variable


def get_info_api(data, keys, default=None):
    for key in keys: 
        if isinstance(data, dict):
            data = data.get(key, default)
        elif isinstance(data, list) and isinstance(key, int) and len(data) > key:
            data = data[key]
        else: 
            return default
    return data

def fetch_weater(lat, lon):
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact.json?lat={lat}&lon={lon}"
    headers = {
        "User-Agent": "MyWeatherApp/1.0  (contact: kristoffersenbendik@gmail.com)"
    }
    response = requests.get(url,headers=headers)
    if response.status_code != HTTPStatus.OK:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

    data = response.json()

    timeseries = get_info_api(data, ['properties', 'timeseries'], [])
    if not timeseries: 
        print("No timeseries data found")
        return None
    
    return timeseries

def parse_weather(timeseries):
    times = []
    temperatures = []
    humidity = []
    wind_speed = []
    wind_dir = []

    for entry in timeseries: 
        if not isinstance(entry, dict): 
           print(f"Skipping non-dict entry in timeseries: {entry}")
           continue 

        time_str = entry.get('time')
        if not time_str:
            print(f"Missing time in entry: {time_str}")
            continue

        try: 
            time_obj = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        except ValueError:
            print(f"Invalid time format: {time_obj}")
            continue

        details = get_info_api(entry, ['data', 'instant', 'details'], {})

        times.append(time_obj)
        temperatures.append(details.get('air_temperature'))
        humidity.append(details.get('relative_humidity'))
        wind_speed.append(details.get('wind_speed'))
        wind_dir.append(details.get('wind_from_direction'))

    return times, temperatures, humidity, wind_speed, wind_dir

def plot_weather(times, temps, hum, wind_speed, wind_dir):
    plt.style.use('seaborn-v0_8-darkgrid')

    fig, axs = plt.subplots(4, 1, figsize=(10,12), sharex=True)

    # Create a colormap gradient from blue to purple
    colors = [cm.plasma(i) for i in [0.1, 0.35, 0.6, 0.85]]

    axs[0].plot(times, temps, label='Temperature (Celsius)', color=colors[0], linewidth=2)
    axs[0].set_ylabel('Temperature (Celsius)', fontsize=12)
    axs[0].legend(loc='upper right', fontsize=10, frameon=True)

    axs[1].plot(times, hum, label='Humidity (%)', color=colors[1], linewidth=2)
    axs[1].set_ylabel('Humidity (%)', fontsize=12)
    axs[1].legend(loc='upper right', fontsize=10, frameon=True)

    axs[2].plot(times, wind_speed, label='Wind Speed (m/s)', color=colors[2], linewidth=2)
    axs[2].set_ylabel('Wind Speed (m/s)', fontsize=12)
    axs[2].legend(loc='upper right', fontsize=10, frameon=True)

    axs[3].plot(times, wind_dir, label='Wind Direction (Degrees)', color=colors[3], linewidth=2)
    axs[3].set_ylabel('Wind Direction (Degrees)', fontsize=12)
    axs[3].legend(loc='upper right', fontsize=10, frameon=True)

    # TODO: Cleanup chart - Not looking very clean atm 
    fig.suptitle(
        'Trondheim Weather Forecast Overview',
        fontsize=16,
        fontweight='bold',
        y=0.98
    )

    # a - Weekday, d - DoM, b - Abbrv. month, H(our):M(in)
    axs[3].xaxis.set_major_formatter(mdates.DateFormatter('%a %d %b %H:%M'))
    plt.xticks(rotation=45, fontsize=10)
    plt.xlabel('Time', fontsize=12)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig("weather_plot.png", dpi=150)
    plt.show() # Show graph  
    plt.close()

'''
Specify user to send attachment to
- Just for example usage and in general learning 
- This program could be scheduled with crontab as well, 
  including sending an email on a daily basis or whenever
- The function assumes same recipient, added in the .env file 
def send_email_attachment(subject, body, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject

    email_user = os.getenv("EMAIL_USER")
    email_pass = kr.get_password("email_service", email_user)
    to_email = os.getenv("EMAIL_RECIPIENT")

    if not email_user or not email_pass or not to_email: 
        raise ValueError("Missing required enviroment variable(s)")

    msg['From'] = email_user
    msg['To'] = to_email
    msg.set_content(body)

    with open(attachment_path, 'rb') as f: 
        file_data = f.read()
        file_name = os.path.basename(f.name)
        msg.add_attachment(file_data, maintype='image',subtype='png', filename=file_name)

    # SSL used as security protocol
    with smlib.SMTP_SSL('smtp.gmail.com', 465) as smtp: 
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)
'''    

if __name__ == "__main__": 
    date = datetime.today().strftime('%Y-%m-%d %H:%M') # '2025-06-03 19:23' 
    lat = 63.370918 # Hardcoded for now, could just be changed to prompt a "user"
    lon = 10.380253
    ts = fetch_weater(lat, lon)
    if ts: 
        times, temps, hums, ws, wd = parse_weather(ts)
        plot_weather(times, temps, hums, ws, wd)
        '''
        send_email_attachment(
            subject=f"Daily Weather Report: {date}",
            body="Attached is the latest weather report for Trondheim",
            attachment_path="weather_plot.png"
        )
        ''' 