from tkinter import *
import requests as req
# import time

root = Tk()

status = StringVar()

city_from_api = StringVar()

time_fajr = StringVar()
time_sunrise = StringVar()
time_luhar = StringVar()
time_asar = StringVar()
time_magrib = StringVar()
time_isha = StringVar()


def set_values(result):
    time_fajr.set(str(result['Fajr']))
    time_sunrise.set(str(result['Sunrise']))
    time_luhar.set(str(result['Dhuhr']))
    time_asar.set(str(result['Asr']))
    time_magrib.set(str(result['Maghrib']))
    time_isha.set(str(result['Isha']))


def find_timings():
    city = entry_city.get()
    if city:
        status.set("found..!")
        url = "https://maps.googleapis.com/maps/api/geocode/json?&address=" + city
        url = url.replace(" ", "+")
        response1 = req.get(url)
        json_res = response1.json()
        # print(json_res)

        c = len(json_res['results'][0]['address_components'])
        for i in range(0, c):
            if "locality" in json_res['results'][0]['address_components'][i]['types']:
                city = json_res['results'][0]['address_components'][i]['long_name']
        for i in range(0, c):
            if "country" in json_res['results'][0]['address_components'][i]['types']:
                country = json_res['results'][0]['address_components'][i]['long_name']

        city_from_api.set(city+", "+country)

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

        method = str(methods[var.get()])

        # final request
        url3 = "http://api.aladhan.com/timings/" + timeStamp + "?latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&timezonestring=" + timeZone + "&method=" + method

        final_res = req.get(url3)
        json_final_res = final_res.json()
        result = json_final_res['data']['timings']
        set_values(result)

    else:
        status.set("City not entered!")


def reset_all():
    entry_city.delete(0, END)
    status.set("Ready")
    time_fajr.set("00:00")
    time_sunrise.set("00:00")
    time_luhar.set("00:00")
    time_asar.set("00:00")
    time_magrib.set("00:00")
    time_isha.set("00:00")
    city_from_api.set("")

root.title("salah mate")
root.resizable(width=False, height=False)

# frames
frame_input = Frame(root)
frame_input.pack(fill=X, padx=30, pady=5)

frame_city = Frame(root)
frame_city.pack()

frame_output = Frame(root, bg="#c4c4c4")
frame_output.pack(fill=X, padx=30, pady=25)

# heading
label_heading = Label(frame_input, text="SALAH MATE", fg="green")
label_heading.grid(row=0, sticky=W, columnspan=2, padx=150, pady=15)

# input elements
label_city = Label(frame_input, text="City:")
label_city.grid(row=1, sticky=E)

label_method = Label(frame_input, text="Method:")
label_method.grid(row=2, sticky=E)
frame_input.columnconfigure(1, weight=1)

entry_city = Entry(frame_input, width=35)
entry_city.grid(row=1, column=1, sticky=W, padx=15, pady=10)

var = StringVar(root)
methods = {
    "Shia Ithna-Ashari": 0,
    "University of Islamic Sciences Karachi": 1,
    "Islamic Society of North America (ISNA)": 2,
    "Muslim World League (MWL)": 3,
    "Umm al-Qura, Makkah" : 4,
    "Egyptian General Authority of Survey": 5,
    "Institute of Geophysics, University of Tehran": 6
}
list_method = OptionMenu(frame_input, var, *methods)
var.set("Institute of Geophysics, University of Tehran")
list_method.grid(row=2, column=1, padx=15, pady=10, sticky=W)

button_calc = Button(frame_input, text="find timings", command=find_timings)
button_calc.grid(row=3, columnspan=2, padx=15, pady=10)

# city info
city_found = Label(frame_city, text="city: ", textvariable=city_from_api).grid(row=0, column=0)


# output elements
label_head = Label(frame_output, text="Today timings", fg="green").grid(row=0, sticky=W, columnspan=2, padx=150, pady=15)
label_1 = Label(frame_output, text="fajr :", bg="#c4c4c4").grid(row=1, column=0, sticky=E)
label_2 = Label(frame_output, text="sunrise :", fg="red", bg="#c4c4c4").grid(row=2, column=0, sticky=E)
label_3 = Label(frame_output, text="luhar :", bg="#c4c4c4").grid(row=3, column=0, sticky=E)
label_4 = Label(frame_output, text="aras :", bg="#c4c4c4").grid(row=4, column=0, sticky=E)
label_5 = Label(frame_output, text="magrib :", bg="#c4c4c4").grid(row=5, column=0, sticky=E)
label_6 = Label(frame_output, text="isha :", bg="#c4c4c4").grid(row=6, column=0, sticky=E)

res_label_1 = Label(frame_output, bg="#c4c4c4", textvariable=time_fajr).grid(padx=15, pady=5, row=1, column=1, sticky=W)
res_label_2 = Label(frame_output, fg="red", bg="#c4c4c4", textvariable=time_sunrise).grid(padx=15, pady=5, row=2, column=1, sticky=W)
res_label_3 = Label(frame_output, bg="#c4c4c4", textvariable=time_luhar).grid(padx=15, pady=5, row=3, column=1, sticky=W)
res_label_4 = Label(frame_output, bg="#c4c4c4", textvariable=time_asar).grid(padx=15, pady=5, row=4, column=1, sticky=W)
res_label_5 = Label(frame_output, bg="#c4c4c4", textvariable=time_magrib).grid(padx=15, pady=5, row=5, column=1, sticky=W)
res_label_6 = Label(frame_output, bg="#c4c4c4", textvariable=time_isha).grid(padx=15, pady=5, row=6, column=1, sticky=W)

reset_button = Button(root, text="RESET", command=reset_all).pack()

time_fajr.set("00:00")
time_sunrise.set("00:00")
time_luhar.set("00:00")
time_asar.set("00:00")
time_magrib.set("00:00")
time_isha.set("00:00")


label_status = Label(root, anchor=W, relief=SUNKEN, textvariable=status).pack(side=BOTTOM, fill=X)
status.set("Ready")

root.geometry("450x540")

root.mainloop()