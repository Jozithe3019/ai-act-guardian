import data_provider

def test_import():
    # Style: import X; X.y()
    rec = data_provider.get_patient_record()
    print(rec) # Should be caught

if __name__ == "__main__":
    test_import()