class MedicalAI:
    def analyze_patient(self, p_name):
        # This is inside a ClassDef and should be caught
        print(p_name)

if __name__ == "__main__":
    ai = MedicalAI()
    ai.analyze_patient("Charlie")