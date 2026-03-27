from data_provider import get_patient_record, global_ssn_data

def run_app():
    # Inheriting taint across files!
    data = get_patient_record()
    ssn = global_ssn_data
    
    # Leak sinks
    print(data)
    print(ssn)

if __name__ == "__main__":
    run_app()
