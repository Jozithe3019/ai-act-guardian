import monai

def leak_logic(patient_record):
    # Taint Source
    p_name = patient_record['patient_name']
    
    # Taint Propagation (Renaming)
    hidden_var = p_name
    
    # Data Sink (Escape!)
    print(f"DEBUG: Processing user {hidden_var}")

if __name__ == "__main__":
    leak_logic({'patient_name': 'Alice'})
