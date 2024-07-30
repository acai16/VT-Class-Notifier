import tkinter as tk
import getData
import json
import os
from tabulate import tabulate
import schedule
import time
import classRefresher
import threading
import textme

filename = "vt_api\\dataObjects.json"
def submit():
    # campus.set("0")
    # termyear.set("202409")
    core_code.set("AR%")
    # subj_code.set("CS")
    schdtype.set("%")
    # crse_number.set("3114")
    # crn.set("")
    open_only.set("on")
    sess_code.set("%")
    inst_name.set("")
    if campus.get() == "Blacksburg":
        campus.set("0")
    elif campus.get() == "Virtual":
        campus.set("10")
    formattedTermyear = termyear.get()[2:7] + termyeardict[termyear.get()[0:2]]
    
    dataObject = getData.getData(
    campus.get(), formattedTermyear, core_code.get(), subj_code.get(), 
    schdtype.get(), crse_number.get(), crn.get(), open_only.get(), 
    sess_code.get(), inst_name.get()
    )
    df = dataObject.parseData()
   # displayData(df)
    print(df.head())
    # Define new attributes
    new_attributes = {
        'campus': campus.get(),
        'termyear': formattedTermyear,
        'core_code': core_code.get(),
        'subj_code': subj_code.get(),
        'schdtype': schdtype.get(),
        'crse_number': crse_number.get(),
        'crn': crn.get(),
        'open_only': open_only.get(),
        'sess_code': sess_code.get(),
        'inst_name': inst_name.get()
    }
    # Load existing data
    existing_data = load_json_file(filename)
    
    # Check if new attributes are already present
    if not attributes_exist(new_attributes, existing_data):
        existing_data.append(new_attributes)
        save_json_file(filename, existing_data)
def stop():
    clear_json_file(filename)
    
def attributes_exist(new_attributes, existing_data):
    return any(
        item == new_attributes for item in existing_data
    )
def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []
def save_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
def displayData(df):
    if (df.empty):
        status_label["text"] = "No classes matching that description"
    else:
        status_label["text"] = tabulate(df[["crn", "course", "instructor", "hours"]], showindex=False, headers = df.columns, tablefmt='psql')
def clear_json_file(filename):
    with open(filename, 'w') as file:
        json.dump([], file, indent=4)    
        
def job():
    listbox.delete(0, tk.END)
    data = load_json_file(filename)
    for item in data:
        dataObject = getData.getData(
            item["campus"],
            item["termyear"],
            item["core_code"],
            item["subj_code"],
            item["schdtype"],
            item["crse_number"],
            item["crn"],
            item["open_only"],
            item["sess_code"],
            item["inst_name"]
        )
        df = dataObject.parseData()
        if df.empty:
            if item["crn"] != "":
                listbox.insert(tk.END, item["crn"])
            else:
                listbox.insert(tk.END, item["subj_code"] + "-" + item["crse_number"] + "CLOSED")
        else:
            listbox.insert(tk.END, df.loc[0, "course"] + ": OPEN")
            textme.send("YOUR CLASS IS OPEN")
        
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every(5).seconds.do(job)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

app = tk.Tk()
app.geometry("600x400")

app.title("Simple GUI")


campus = tk.StringVar()
termyear = tk.StringVar()
core_code = tk.StringVar()
subj_code = tk.StringVar()
schdtype = tk.StringVar()
crse_number = tk.StringVar()
crn = tk.StringVar()
open_only = tk.StringVar()
sess_code = tk.StringVar()
inst_name = tk.StringVar()


campus_options = ["Blacksburg", "Virtual"]

campus.set(campus_options[0])# default value

campus_dropdown = tk.OptionMenu(app, campus, *campus_options)

campus_label = tk.Label(app, text='Campus', font=('calibre', 10, 'bold'))
campus_entry = tk.Entry(app, textvariable=campus, font=('calibre', 10, 'normal'))


termyeardict = {
    "FA": "09",
    "SP": "03",
    "SU": "06"
}

listbox = tk.Listbox(app, height=10)

termyear_label = tk.Label(app, text='Term Year', font=('calibre', 10, 'bold'))
termyear_entry = tk.Entry(app, textvariable=termyear, font=('calibre', 10, 'normal'))
termyear_instruction = tk.Label(app, text='[FA, SP, SU] + YYYY, e.g. FA2024')
core_code_label = tk.Label(app, text='Core Code', font=('calibre', 10, 'bold'))
core_code_entry = tk.Entry(app, textvariable=core_code, font=('calibre', 10, 'normal'))

subj_code_label = tk.Label(app, text='Subject Code', font=('calibre', 10, 'bold'))
subj_code_entry = tk.Entry(app, textvariable=subj_code, font=('calibre', 10, 'normal'))

schdtype_label = tk.Label(app, text='Schedule Type', font=('calibre', 10, 'bold'))
schdtype_entry = tk.Entry(app, textvariable=schdtype, font=('calibre', 10, 'normal'))

crse_number_label = tk.Label(app, text='Course Number', font=('calibre', 10, 'bold'))
crse_number_entry = tk.Entry(app, textvariable=crse_number, font=('calibre', 10, 'normal'))

crn_label = tk.Label(app, text='CRN', font=('calibre', 10, 'bold'))
crn_entry = tk.Entry(app, textvariable=crn, font=('calibre', 10, 'normal'))

open_only_label = tk.Label(app, text='Open Only', font=('calibre', 10, 'bold'))
open_only_entry = tk.Entry(app, textvariable=open_only, font=('calibre', 10, 'normal'))

sess_code_label = tk.Label(app, text='Session Code', font=('calibre', 10, 'bold'))
sess_code_entry = tk.Entry(app, textvariable=sess_code, font=('calibre', 10, 'normal'))

inst_name_label = tk.Label(app, text='Instructor Name', font=('calibre', 10, 'bold'))
inst_name_entry = tk.Entry(app, textvariable=inst_name, font=('calibre', 10, 'normal'))

status_label = tk.Label(app, text='', font=('Consolas', 10))

sub_btn = tk.Button(app, text='Submit', command=submit)
clear_button = tk.Button(app, text='Stop All', command=stop)

campus_label.grid(row=0, column=0)
campus_dropdown.grid(row=0, column=1)

termyear_label.grid(row=1, column=0)
termyear_entry.grid(row=1, column=1)
termyear_instruction.grid(row=1, column=2)


# core_code_label.grid(row=2, column=0)
# core_code_entry.grid(row=2, column=1)

subj_code_label.grid(row=3, column=0)
subj_code_entry.grid(row=3, column=1)

# schdtype_label.grid(row=4, column=0)
# schdtype_entry.grid(row=4, column=1)

crse_number_label.grid(row=5, column=0)
crse_number_entry.grid(row=5, column=1)

crn_label.grid(row=6, column=0)
crn_entry.grid(row=6, column=1)

# open_only_label.grid(row=7, column=0)
# open_only_entry.grid(row=7, column=1)

# sess_code_label.grid(row=9, column=0)
# sess_code_entry.grid(row=9, column=1)

# inst_name_label.grid(row=10, column=0)
# inst_name_entry.grid(row=10, column=1)

sub_btn.grid(row=11, column=1)
clear_button.grid(row=12, column=1)
status_label.grid(row=12, column=2)
listbox.grid(row=13, column=1)

app.mainloop()
