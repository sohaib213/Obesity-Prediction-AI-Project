import pandas as pd

data = pd.read_csv("train_dataset.csv")
testing_data = pd.read_csv("test_dataset.csv")


#delete dublicated rows
data = data.drop_duplicates()


#fill nulls
data['FCVC'] = data['FCVC'].fillna(data['FCVC'].mean())
data['CALC'] = data['CALC'].fillna(data['CALC'].mode()[0])


# convert string to int values
GenderMap = {
    'Male': 1,
    'Female': 0
}

data['Gender'] = data['Gender'].map(GenderMap)
testing_data['Gender'] = testing_data['Gender'].map(GenderMap)

yes_no_map = {
    "yes": 1,
    "no": 0
}
data['family_history_with_overweight'] = data['family_history_with_overweight'].map(yes_no_map)
testing_data['family_history_with_overweight'] = testing_data['family_history_with_overweight'].map(yes_no_map)

data['FAVC'] = data['FAVC'].map(yes_no_map)
testing_data['FAVC'] = testing_data['FAVC'].map(yes_no_map)

Frequency_map = {
    'no': 0,
    'Sometimes': 3,
    'Frequently': 6,
    'Always': 10
}
data['CAEC'] = data['CAEC'].map(Frequency_map)
testing_data['CAEC'] = testing_data['CAEC'].map(Frequency_map)

data['SMOKE'] = data['SMOKE'].map(yes_no_map)
testing_data['SMOKE'] = testing_data['SMOKE'].map(yes_no_map)

data['SCC'] = data['SCC'].map(yes_no_map)
testing_data['SCC'] = testing_data['SCC'].map(yes_no_map)

data['CALC'] = data['CALC'].map(Frequency_map)
testing_data['CALC'] = testing_data['CALC'].map(Frequency_map)

transportaion_map = {
    'Automobile': 0,
    'Public_Transportation': 1,
    'Motorbike': 2,
    'Bike': 3,
    'Walking': 4
}
data['MTRANS'] = data['MTRANS'].map(transportaion_map)
testing_data['MTRANS'] = testing_data['MTRANS'].map(transportaion_map)


weight_map = {
    'Insufficient_Weight': 0,
    'Normal_Weight': 1,
    'Overweight_Level_I': 2,
    'Overweight_Level_II': 3,
    'Obesity_Type_I': 4,
    'Obesity_Type_II': 5,
    'Obesity_Type_III': 6
}
data['NObeyesdad'] = data['NObeyesdad'].map(weight_map)
testing_data['NObeyesdad'] = testing_data['NObeyesdad'].map(weight_map)

X = data.drop(columns=['NObeyesdad'])
Y = data['NObeyesdad']

X_Test = testing_data.drop(columns=["NObeyesdad"])
Y_Test = testing_data['NObeyesdad']

#feature selection
X = X.drop(columns=["SMOKE"])
X_Test = X_Test.drop(columns=["SMOKE"])


#Gradient Boosting
from sklearn.ensemble import GradientBoostingClassifier
# Initialize the model
model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
# Train the model
model.fit(X, Y)



from tkinter import *

window = Tk()
window.geometry("1920x1000")
window.title("Obesity Prediction App")
backgroundColor = 'Black'
window.configure(background=backgroundColor)
window.state('zoomed')


# Welcome Label
Label(window,
      text="Welcome to the Obesity Prediction App",
      font=('Helvetica', 24, 'bold'),
      bg='#2a2a40',           # deep blue-gray
      fg='#00ffcc',           # bright teal
      padx=20,
      pady=20,
      bd=8,
      relief=GROOVE).pack(pady=40)

# Master frame to hold all sections horizontally
first_frame = Frame(window, background=backgroundColor)
second_frame = Frame(window, background=backgroundColor)
third_frame = Frame(window, background=backgroundColor)
first_frame.pack(ipadx=50, side=LEFT)
second_frame.pack(ipadx=50, side=LEFT)
third_frame.pack(ipady=50, side=LEFT)


# Function to create a section (label + inputs) horizontally
def create_section(parent, label_text):
    frame = Frame(parent, padx=30, relief=GROOVE, background=backgroundColor)

    frame.pack(fill=Y, padx=10)
    Label(frame, text=label_text,
          font=('Arial', 20, 'bold'),
          foreground="blue",
          # background="#2a2a40",
          background="black",
          padx=5,
          pady=5).pack(pady=40, padx=10, side=LEFT)

    return frame


yes_no_map = {
    "yes": 1,
    "no": 0
}
def createRadioButton(frame, label_text, map):
    selected_option = StringVar()
    selected_option.set('1')
    frame = create_section(frame, label_text)
    Label(frame, background=backgroundColor).pack(pady=2)
    for label, value in map.items():
        radio = Radiobutton(
            frame,
            text=label,
            variable=selected_option,
            value=value,
            bg=backgroundColor,
            fg='white',
            activeforeground='white',
            activebackground=backgroundColor,
            selectcolor='gray20',
            font=20
        )
        radio.pack(anchor='w')
    return  selected_option

def createOptionMenu(frame, label_text, map, default_value):
    selected_option = StringVar()
    selected_option.set(default_value)
    caec_frame = create_section(frame, label_text)
    optionMenu = OptionMenu(caec_frame, selected_option, *map)
    optionMenu.config(bg=backgroundColor, foreground="white", activeforeground=backgroundColor, font=20)
    optionMenu.pack(pady=45)
    return  selected_option

def createNumberField(frame, label_text):
    s_frame = create_section(frame, label_text)
    validate_cmd = window.register(validate_input)
    ageFiled = Entry(s_frame, validate="key", font=20, width=maxLength, validatecommand=(validate_cmd, '%P', '%S'))
    ageFiled.pack(pady=50)
    return ageFiled

maxLength = 6
def validate_input(P, S):
    if ((P == '' or S.isdigit() or S == '.')  and len(P) <= maxLength):
        return True
    else:
        return False
# --- Gender ---
GenderMap = {
    'Male': 1,
    'Female': 0
}
gender_selected_option = createRadioButton(first_frame, "Gender", GenderMap)

# --- AGE ---
ageFiled = createNumberField(first_frame, "AGE")

# -- Height ---
heightFiled = createNumberField(first_frame, "Height")

# -- Weight ---
weightFiled = createNumberField(first_frame, "Weight")

# --- Family History ---
family_history_selected_option = createRadioButton(first_frame, "Family History", yes_no_map)

# --- FAVC ---
FAVC_selected_option = createRadioButton(first_frame, "FAVC", yes_no_map)

# -- FCVC ---
FCVCFiled = createNumberField(second_frame, "FCVC")

# -- NCP ---
NCPFiled = createNumberField(second_frame, "NCP")

# --- CAEC ---
CAEC_selected_option = createOptionMenu(second_frame, "CAEC", Frequency_map, 'no')

# --- SMOKE ---
SMOKE_selected_option = createRadioButton(second_frame, "SMOKE", yes_no_map)

# -- CH2O ---
CH2OFiled = createNumberField(second_frame, "CH2O")

# --- SCC ---
SCC_selected_option = createRadioButton(second_frame, "SCC", yes_no_map)

# -- FAF ---
FAFFiled = createNumberField(third_frame, "FAF")

# -- TUE ---
TUEFiled = createNumberField(third_frame, "TUE")

# --- CALC ---
CALC_selected_option = createOptionMenu(third_frame, "CALC", Frequency_map, 'no')

# --- MITRANS ---
MITRANS_selected_option = createOptionMenu(third_frame, "MITRANS", transportaion_map, 'Walking')


warningLabel = Label(window, text="Please Fill All Fields required", font=('Arial', 20, 'bold'), background=backgroundColor,
      foreground="Red")
resultLabel = Label(window, font=('Arial', 20, 'bold'), background=backgroundColor,foreground="Green")



# --- Submit Button ---
def submit():
    if ageFiled.get() == '' or heightFiled.get() == '' or weightFiled.get() == '' or FCVCFiled.get() == '' or NCPFiled.get() == '' or CH2OFiled.get() == '' or FAFFiled.get() == '' or TUEFiled.get() == '':
        warningLabel.pack()
        resultLabel.pack_forget()
        return
    data = {
        "Gender": int(gender_selected_option.get()),
        "Age": int(ageFiled.get()),
        "Height": float(heightFiled.get()),
        "Weight": float(weightFiled.get()),
        "family_history_with_overweight": int(family_history_selected_option.get()),
        "FAVC": int(FAVC_selected_option.get()),
        "FCVC": float(FCVCFiled.get()),
        "NCP": float(NCPFiled.get()),
        "CAEC": Frequency_map[CAEC_selected_option.get()],
        "CH2O": float(CH2OFiled.get()),
        "SCC": int(SCC_selected_option.get()),
        "FAF": float(FAFFiled.get()),
        "TUE": float(TUEFiled.get()),
        "CALC": Frequency_map[CALC_selected_option.get()],
        "MTRANS": transportaion_map[MITRANS_selected_option.get()]
    }
    x_predict = pd.DataFrame([data])
    y_predict = model.predict(x_predict)
    for result in weight_map:
        if y_predict == weight_map[result]:
            resultLabel.config(text=result)
            resultLabel.pack()
            print("Label: ", result, ", Value: ", weight_map[result])

    warningLabel.pack_forget()

Button(window, text="Submit", font=("Arial", 16), command=submit).pack(pady=100)

window.mainloop()