import requests as req

def main():

    print(""""
    *****************************************
    ***************SALAH MATE****************
    *****************************************
    **** Where ever are you in the world ****
    ***** get the accurate prayer times *****
    *****************************************
    *****************************************
    *********** -powered by aladhanapi.com **

    """)

    city_entered = input("enter the city: ")
    json_res = find_city_country(city_entered)

    c = len(json_res['results'][0]['address_components'])
    for i in range(0, c):
        if "locality" in json_res['results'][0]['address_components'][i]['types']:
            city = json_res['results'][0]['address_components'][i]['long_name']
    for i in range(0, c):
        if "country" in json_res['results'][0]['address_components'][i]['types']:
            country = json_res['results'][0]['address_components'][i]['long_name']

    latitude = json_res['results'][0]['geometry']['location']['lat']
    longitude = json_res['results'][0]['geometry']['location']['lng']

    url2 = "http://api.aladhan.com/cityInfo?city=" + city + "&country=" + country
    url2 = url2.replace(" ", "+")

    res_TZ = req.get(url2)
    json_res_TZ = res_TZ.json()
    timeZone = json_res_TZ['data']['timezone']

    res_TS = req.get("http://api.aladhan.com/currentTimestamp?zone=" + timeZone)

    json_res_TS = res_TS.json()
    timeStamp = json_res_TS['data']

    method = get_method()

    # final request
    url3 = "http://api.aladhan.com/timings/" + timeStamp + "?latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&timezonestring=" + timeZone + "&method=" + method

    final_res = req.get(url3)
    json_final_res = final_res.json()
    result = json_final_res['data']['timings']
    print_output(result)


def find_city_country(city_entered):
    url = "https://maps.googleapis.com/maps/api/geocode/json?&address=" + city_entered
    url = url.replace(" ", "+")
    response1 = req.get(url)
    json_res = response1.json()
    return json_res

def get_method():
    print("""
        0 - Shia Ithna-Ashari
        1 - University of Islamic Sciences, Karachi
        2 - Islamic Society of North America (ISNA)
        3 - Muslim World League (MWL)
        4 - Umm al-Qura, Makkah
        5 - Egyptian General Authority of Survey
        7 - Institute of Geophysics, University of Tehran
        """)

    method = input("enter the method code: ")
    return method

def print_output(result):
    print("\nFajr:", result['Fajr'])
    print("Sunrise:", result['Sunrise'])
    print("Dhuhr:", result['Dhuhr'])
    print("Asr:", result['Asr'])
    print("Maghrib:", result['Maghrib'])
    print("Isha:", result['Isha'])
    print("Midnight:", result['Midnight'])

if __name__ == '__main__':
    main()