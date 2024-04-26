import requests  # Import requests library for making HTTP requests
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddressForm, FarmDetailsForm
from .models import FarmModel


from django.shortcuts import render
from .models import FarmModel

map_token = 'pk.eyJ1IjoiZnJhbnpnYWJpamFuIiwiYSI6ImNsdmV3dTljbTBlbzkya3BlY2Rwa28xczgifQ.z1HHDbS-prv9A3gwQJK43A'

def show_map(request):
    # Get all the farms from the database
    farms = FarmModel.objects.all()

    # Calculate the center of the map based on the farms' coordinates
    # center_latitude = sum(farm.latitude for farm in farms) / len(farms)
    # center_longitude = sum(farm.longitude for farm in farms) / len(farms)

    # Pass the necessary data to the template
    context = {
        'farms': farms,
        # 'center_latitude': center_latitude,
        # 'center_longitude': center_longitude,
        'mapbox_access_token': map_token,
    }
    return render(request, 'map.html', context)


def add_farm(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        farmdetails_form = FarmDetailsForm(request.POST)
        if address_form.is_valid() and farmdetails_form.is_valid():
            address_instance = address_form.save(commit=False)
            farmdetails_instance = farmdetails_form.save(commit=False)

            # Combine address fields into a single string
            address = f"{address_instance.barangay}, {address_instance.city_or_municipality}, {address_instance.country}"

            # Call the geocode function to get coordinates
            coordinates = geocode(address)


            if coordinates:
                farm_instance = FarmModel(
                    barangay=address_instance.barangay,
                    city_or_municipality=address_instance.city_or_municipality,
                    country=address_instance.country,
                    acres=farmdetails_instance.acres,
                    crops_planted=farmdetails_instance.crops_planted,
                    latitude=coordinates['latitude'],
                    longitude=coordinates['longitude'],
                )
                farm_instance.save()

                context = {'address_form': address_form, 'details_form': farmdetails_form, 'coordinates': coordinates}

                # Redirect to the same page to maintain the map and marker
                return render(request, 'add_farm.html', context)
            else:
                print('Error: coordinates not obtained')

        else:
            print('Error: data is not valid')

       
    else: 
        #if data form is empty
        print("error: no input")
        address_form = AddressForm()
        farmdetails_form = FarmDetailsForm()
    
    context= {'address_form': address_form, 'details_form': farmdetails_form, 'coordinates': False}

    return render(request, 'add_farm.html', context)


def geocode(address):
    """
    Function to geocode an address using Mapbox's Geocoding API.
    Returns the latitude and longitude coordinates as a dictionary.
    """

    # API endpoint for geocoding
    GEOCODING_API_ENDPOINT = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"

    # Parameters for the API request
    params = {
        'access_token': map_token
    }

    # Make a GET request to the Geocoding API
    response = requests.get(GEOCODING_API_ENDPOINT, params=params)

    # Parse the JSON response
    data = response.json()

    # Extract latitude and longitude from the response
    if 'features' in data and len(data['features']) > 0:
        coordinates = data['features'][0]['geometry']['coordinates']
        return {'latitude': coordinates[1], 'longitude': coordinates[0]}
    else:
        return {'latitude': None, 'longitude': None}




def view_farms(request):
    farms = FarmModel.objects.all()
    return render(request, 'view_farms.html', {'farms': farms})


def update_farm(request, farm_id):
    # Retrieve the farm instance
    farm = get_object_or_404(FarmModel, pk=farm_id)

    if request.method == 'POST':
        # Bind the POST data to the forms instances
        address_form = AddressForm(request.POST, instance=farm)
        farmdetails_form = FarmDetailsForm(request.POST, instance=farm)
        if address_form.is_valid() and farmdetails_form.is_valid():
            # Save the forms to update the farm instance
            address_form.save()
            farmdetails_form.save()
            return redirect('view_farms')
    else:
        # Create form instances and pass the farm instance as the initial data
        address_form = AddressForm(instance=farm)
        farmdetails_form = FarmDetailsForm(instance=farm)
    
    context ={'address_form': address_form, 'farmdetails_form': farmdetails_form, 'farm': farm}

    # Render the template with the forms
    return render(request, 'update_farm.html', context)



def delete_farm(request, farm_id):
    # Retrieve the farm instance
    farm = FarmModel.objects.get(farm_id=farm_id)
    if request.method == 'POST':
        # Delete the farm instance
        farm.delete()
        return redirect('view_farms')
    return render(request, 'delete_farm.html', {'farm': farm})



