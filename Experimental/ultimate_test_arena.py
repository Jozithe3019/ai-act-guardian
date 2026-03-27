def anonymize(x): return "XXX"

def good_function(patient_name):
    # This should be CLEAN after anonymization
    p_safe = anonymize(patient_name)
    print(p_safe) 

def bad_function(patient_name):
    # This should be a CRITICAL leak
    print(patient_name)

def deceptive_function():
    # Art 52 violation
    is_ai_generated = False
    return "Hello"

if __name__ == "__main__":
    good_function("Alice")
    bad_function("Bob")
