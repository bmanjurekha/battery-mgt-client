import requests
import json
import time
import matplotlib.pyplot as plt



def make_request(endpoint,method, data):
    url= "http://127.0.0.1:5000/"+endpoint
    if method=="GET":
        response = requests.get(url)
    elif method=="POST":
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
    return response

def display_response(get_response):
    print("Request Sent:")
    print(f"Status Code: {get_response.status_code}")
    print("Response JSON:")
    print(get_response.json())
    print("\n")
    
   
def display_information():
    # Display the times of the day and total energy consumption
    url="info"
    response_info = make_request(url,"GET","")
    info_data = response_info.json()

    print("\nTimes of the Day and Total Energy Consumption:")
    print(f"Time (HH:MM): {info_data['sim_time_hour']:02d}:{info_data['sim_time_min']:02d}")
    print(f"Total Energy Consumption: {info_data['base_current_load']} kW\n")

def display_optimization():
    # Display how charging is optimized
    url="priceperhour"
    response_price = make_request(url,"GET","")
    url="baseload"
    response_base_load = make_request(url,"GET","")
    price_data = response_price.json()
    base_load_data = response_base_load.json()

    print("Optimization Visualization:")
    for hour in range(len(price_data)):
        print(f"{hour:02d}:00 - {hour+1:02d}:00 | Energy Price: {price_data[hour]} SEK/kWh | Base Load: {base_load_data[hour]} kW")
    print("\n")

if __name__ == "__main__":
    while True:
        #User has to select below option to perform operation
        print ("================================================================")
        print ("Select below options")
        print ("1.Default - EV Battery capacity kwh")
        print ("2.Information - Get information about what power the charging station can handle?")
        print ("3.Baseload - Household's energy consumption during a 24-hour period ")
        print ("4.Price per hour - Nordpool's hourly price 00:00 - 24:00")
        print ("5.Start Charge")
        print ("6.Stop Charge")
        print ("7.Discharge to 20%")
        print ("8.Charge Status")
        print ("9.Charge when the electricity price is at its lowest and the household's consumption does not exceed 11 kW (three-phase-16A)")
        print ("10.Charge Battery between 20-80%")
        print ("11.Times of the day and total energy consumption and show how loading is optimized")
    
        url=""
        def case1():
            
            # Example GET request - Default
            url = ""            
            get_response = make_request(url,"GET","")            
            display_response(get_response)

        def case2():
            url ="info"       
            get_response = make_request(url,"GET","")            
            display_response(get_response)

        def case3():
            url ="baseload"       
            get_response = make_request(url,"GET","")            
            display_response(get_response)
            
        def case4():
            url ="priceperhour"  
            get_response = make_request(url,"GET","")            
            display_response(get_response)
            
        def case5():
            url="charge"
            post_data = {"charging":"on"}
            get_response = make_request(url,"POST",post_data)
            display_response(get_response)
            
        def case6():
            url="charge"
            post_data = {"charging":"off"}
            get_response = make_request(url,"POST",post_data)
            display_response(get_response)
        
        def case7():
            url="discharge"
            post_data = {"discharging":"on"}
            get_response = make_request(url,"POST",post_data)
            display_response(get_response)
        
        def case8():
            url ="charge"       
            get_response = make_request(url,"GET","")            
            display_response(get_response)
            
        def case9():
            # Check household consumption and energy price
            url = "info"
            get_response = make_request(url,"GET","") 
            current_consumption = get_response.json().get("base_current_load", 0)
            
            url="priceperhour"
            get_response = make_request(url,"GET","")
            energy_prices = get_response.json()
             # Determine the lowest electricity price
            lowest_price = min(energy_prices)
            # Check conditions for starting charging
            if (
                current_consumption <= 11 and  # Check household consumption limit
                lowest_price == energy_prices[0]  # Check if the current price is the lowest
            ):
                # Start charging when conditions are met
                url="charge"
                post_data = {"charging":"on"}
                start_response = make_request(url,"POST",post_data)
                print("Start Charging Response:")
                display_response(start_response)
            else:
                print("Charging conditions not met. Charging is not started.")

            # Simulate some time passing
            time.sleep(5)

            # Stop charging
            url="charge"
            post_data = {"charging":"off"}
            stop_response =  make_request(url,"POST",post_data)
            print("Stop Charging Response:")
            display_response(stop_response)

            # Check battery status
            url = "info"
            battery_status = make_request(url,"GET","")
            print("Battery Status:")
            display_response(battery_status)

        def case10():
            try:
                # Read initial battery capacity
                url = "info"
                initial_battery_status = make_request(url,"GET","")
                initial_capacity_percent = initial_battery_status.json().get("battery_capacity_kWh", 0)

                print("Initial Battery Capacity:", initial_capacity_percent, "%")

                # Charge the battery from 20% to 80%
                target_capacity_percent = 80
                while initial_capacity_percent < target_capacity_percent:
                    # Start charging
                    url="charge"
                    post_data = {"charging":"on"}
                    start_response = make_request(url,"POST",post_data)
                    print("Start Charging Response:")
                    display_response(start_response)

                    # Simulate some time passing
                    #time.sleep(5)

                    # Read current battery capacity
                    url = "info"
                    current_battery_status = make_request(url,"GET","")
                    current_capacity_percent = current_battery_status.json().get("battery_capacity_kWh", 0)

                    print("Current Battery Capacity:", current_capacity_percent, "%")

                    # Stop charging if the target capacity is reached
                    if current_capacity_percent >= target_capacity_percent:
                        url="charge"
                        post_data = {"charging":"off"}
                        stop_response = make_request(url,"POST",post_data)
                        print("Stop Charging Response")
                        display_response(stop_response)
                    else:
                        print("Charging in progress...")

                    # Update initial capacity for the next iteration
                    initial_capacity_percent = current_capacity_percent

            except requests.exceptions.RequestException as e:
                print("Error:", e)
        def case11():
                    
                    # Check household consumption and energy price
                    url="info"
                    get_response = make_request(url,"GET","")
                    get_household_consumption = get_response.json().get("base_current_load", 0)
                    hourly_consumption = [get_household_consumption for _ in range(24)]
                    
                    url="priceperhour"
                    get_response = make_request(url,"GET","")
                    energy_price = get_response.json()
                    
                    
                    url="charge"
                    post_data = {"charging":"on"}
                    start_response = make_request(url,"POST",post_data)
                    print("Start Charging Response")
                    display_response(start_response)

                    # Simulate some time passing
                    time.sleep(5)

                    # Stop charging
                    url="charge"
                    post_data = {"charging":"off"}
                    stop_response = make_request(url,"POST",post_data)
                    print("Stop Charging Response")
                    display_response(stop_response)
                    
                    # # Display information after stopping charging
                    display_information()

                    # Check battery status
                    url="info"
                    battery_status = make_request(url,"GET","")
                    print("Battery Status")
                    display_response(battery_status)

                    # Display optimization visualization
                    display_optimization()
        def default_case():
            return "No Option Selected"            
            

        def switch_case(case_value):
            switch_dict = {
                1: case1,
                2: case2,
                3: case3,
                4: case4,
                5: case5,
                6: case6,
                7: case7,
                8: case8,
                9: case9,
                10: case10,
                11: case11
            }

            # Use the get() method with a default value to handle the default case
            selected_case = switch_dict.get(case_value, default_case)

            # Execute the selected function and return its result
            return selected_case()
        
        # Get user input and store it in a variable
        user_input = int(input("Enter : "))

        # Print the user input
        print("You have selected:", user_input)

        result = switch_case(user_input)
     