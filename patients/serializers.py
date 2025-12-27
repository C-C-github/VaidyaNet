class AdminPatientMaskedSerializer:
    """
    Admin is allowed to see ONLY:
    - patient_id
    - problem_summary
    """

    def __init__(self, patient):
        self.data = {
            "patient_id": patient.id,
            "problem_summary": patient.problem_summary,
        }
