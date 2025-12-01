import pandas as pd
import numpy as np

FEATURES = [
    'age', 'height', 'weight', 'ap_hi', 'ap_lo',
    'smoke', 'alco', 'active',
    'gender_2',
    'cholesterol_2', 'cholesterol_3',
    'gluc_2', 'gluc_3',
    'BMI',
    'bmi_obeso', 'bmi_sottopeso', 'bmi_sovrappeso'
]

def preprocess_input(age, height, weight, ap_hi, ap_lo,
                     gender, cholesterol, gluc, smoke, alco, active):

    # Dizionario 
    row = {
        "age": age,
        "height": height,
        "weight": weight,
        "ap_hi": ap_hi,
        "ap_lo": ap_lo,
        "smoke": smoke,
        "alco": alco,
        "active": active,
    }

    # Dummy: gender 
    row["gender_2"] = 1 if gender == 2 else 0

    # Dummy: cholesterol
    row["cholesterol_2"] = 1 if cholesterol == 2 else 0
    row["cholesterol_3"] = 1 if cholesterol == 3 else 0

    # Dummy: gluc
    row["gluc_2"] = 1 if gluc == 2 else 0
    row["gluc_3"] = 1 if gluc == 3 else 0

    # BMI
    BMI = weight / ((height/100)**2)
    row["BMI"] = BMI

    # Dummy: categorie BMI
    row["bmi_obeso"] = 1 if BMI >= 30 else 0
    row["bmi_sovrappeso"] = 1 if 25 <= BMI < 30 else 0
    row["bmi_sottopeso"] = 1 if BMI < 18.5 else 0

    # Convertire in DF con colonne in ordine corretto
    df = pd.DataFrame([row])
    return df[FEATURES]
