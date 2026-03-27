def handle_data(record):
    # 1. Deception
    is_ai_generated = False 
    
    # 2. Taint and Sanitization
    p_name = record['patient_name']
    p_name = "REDACTED" # This should clear the taint
    
    # 3. This should NOT be a leak finding
    print(p_name) 
    
    # 4. But this IS a leak finding (direct from param)
    print(record)

if __name__ == "__main__":
    handle_data({'patient_name': 'Secret'})
