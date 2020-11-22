import numpy as np
from scipy.io import loadmat

file_path = ('/flask/data/Q0001')

def get_features(file_name):
    
    #data_dict {fs, n_samples,"age","sex","output":[0 1 0 1 0],"prescript","hist","sympt", 
    #leads:[{"gain","name",samples:[]}]}

    #Cargamos los datos de los archivos y los inicializamos con NumPy
    data_dict = {}
    data = np.asarray(loadmat(file_name + ".mat")['val'], dtype = np.float64)
    
    #Abrimos el archivo .hea
    with open(file_name + ".hea",'r') as f:
        header_data = f.readlines()

    #De la primera linea extraemos la informacion relevante
    archivo ,n_leads ,fs,n_samples ,_ ,_ = header_data[0].split()
    #Mapeamos el output de arriba con los valores relevantes de este
    n_leads, fs, n_samples = map(int, [n_leads, fs, n_samples])
    #Cada uno de estos los almacenamos en un diccionario 
    data_dict["archivo"] = archivo
    data_dict["n_leads"] = n_leads
    data_dict["fs"] = fs
    data_dict["n_samples"] = n_samples
    data_dict["leads"] = []
    #por ejemplo data_dict --> {'n_leads': 12, 'fs': 500, 'n_samples': 7500, 'leads': []}

    #Iteramos a través del numero de derivaciones
    for i in range(n_leads):

        tmp = header_data[i + 1].split()

        #Nombre de la derivacion sobre la que se itera
        lead_name = tmp[-1].replace("\n","")

        #Amplitude resolution
        gain_mv = int(tmp[2].lower().replace("/mv",""))

        #Guardamos todos los valores en una nueva variable lead y la añadimos 
        #a nuestro diccioanrio
        lead = {}
        lead["name"] = np.where(lead_names == lead_name)[0]
        lead["gain_mv"] = gain_mv
        lead["samples"] = data[i]
        data_dict["leads"].append(lead)

    #A continuación se itera sobre todo el documendo .hea para extraer datos 
    #sobre edad, sexo y la enfermedad
    for line in header_data:

        #Extraemos la edad
        if "#Age" in line:
            age = line.split(": ")[1]
            #Guardamos la edad y si esta no esta registrada le asignamos un valor arbitrario
            data_dict["age"] = int(age if not "NaN" in age else 57)
        #Extraemos el sexo si es (Masculino 0) si es (femenino 1)
        elif "#Sex" in line:
            data_dict["sex"] = 0 if line.split(": ")[1].replace("\n","") == "Male" else 1
        #IMPORTANTE 
        #Extraemos la clase 
        #Almacena el resultado de dicha clase en un array de N posiciones 
        #que se corresponden con las N posibles clases del csv
        elif "#Dx" in line:
            data_dict["output"] = np.zeros((1,len(csv_file['Abbreviation'])))
            for c in line.split(": ")[1].replace("\n","").split(","):
              for x in range(len(csv_file.index)):
                if (int(csv_file['SNOMED CT Code'][x]) == int(c)):
                  data_dict["output"][0][x] = 1
        #Info de RX Hx y Sx en el .hea
        elif "#Rx" in line:
            data_dict["Rx"] = line.split(": ")[1].replace("\n","")
        elif "#Hx" in line:
            data_dict["Hx"] = line.split(": ")[1].replace("\n","")
        elif "#Sx" in line:
            data_dict["Sx"] = line.split(": ")[1].replace("\n","")

    return data_dict


aux = get_features(file_path)
