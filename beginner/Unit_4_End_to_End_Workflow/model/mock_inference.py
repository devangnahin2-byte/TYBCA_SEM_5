
class AdmissionModelMock:
    def __init__(self):
        self.accuracy = 0.85
        print("Model initialized.")
        
    def predict_admission(self, student_data):
        """
        Takes student dictionary, returns mock prediction.
        """
        score = student_data.get("score", 0)
        
        if score > 50:
            return "Eligible for Admission"
        return "Waitlisted"

if __name__ == "__main__":
    print("Testing Mock Inference Model...")
    model = AdmissionModelMock()
    
    test_student = {"name": "Test", "score": 75}
    result = model.predict_admission(test_student)
    
    print(f"Result for student with score {test_student['score']}: {result}")
