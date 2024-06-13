from prefect import flow,task
from yr_weather.data.locationforecast import ForecastTimeDetails, ForecastFutureDetails
from yr_weather.locationforecast import Locationforecast

nis_lat = 43.32472
nis_lon = 21.90333

@flow
def adapt_inside_temperature(lat, lon):
    inside_temp_in_C = get_inside_temperature()
    location_forecast = connect_to_weather_api(lat, lon)
    make_changes(location_forecast, inside_temp_in_C, lat, lon)
    
@flow
def connect_to_weather_api(lat, lon):
    headers = {
        'User-Agent': 'CentralHeatingSystemAgent 1.0',
        'From': 'github.com/Nemanja1996S/CentralHeatingSystem'  
    }
    return Locationforecast(headers=headers)

@task
def get_inside_temperature():
    return 10

@flow
def make_changes(location_forecast: Locationforecast, inside_temp_in_C: int, lat, lon):
    forecast = location_forecast.get_forecast(lat, lon)

    forecast_now = forecast.now()
    forecast_details = forecast_now.details
    
    forecast_next_hour = forecast_now.next_hour
    forecast_next_hour_details = forecast_next_hour.details
    
    print(str(forecast_next_hour_details))

    compare_details(forecast_details, forecast_next_hour_details, inside_temp_in_C)

@task
def compare_details(forecast_now : ForecastTimeDetails, forecast_next_hour: ForecastFutureDetails, inside_temp_in_C: int, desired_temperature = 20):

    current_temperature = forecast_now.air_temperature
    next_hour_temperature = forecast_next_hour.air_temperature

    current_humidity = forecast_now.relative_humidity
    next_hour_humidity = forecast_next_hour.relative_humidity

    if (inside_temp_in_C - 5 < current_temperature) or (inside_temp_in_C < desired_temperature):
        if(current_humidity > 50) or (next_hour_humidity > 50):
            turn_on_heater(desired_temperature - 2)
            return
        elif(next_hour_temperature < desired_temperature):
            turn_on_heater(desired_temperature)
            return
        else:
            turn_off_heater()
            return
    else:
        turn_off_heater()
        return
@task    
def turn_on_heater(temperatture: int):
    print('Heater running on ' + str(temperatture) + ' C degrees')
    
@task
def turn_off_heater():
    print('Heater turning off')

adapt_inside_temperature(nis_lat, nis_lon)
