class IrrigationAdvisory:
    def __init__(self):
        # Base irrigation rules defined by crop and growth stage
        pass

    def recommend(self, crop, ndmi, moisture_stress, growth_stage):
        """
        Rule-based irrigation recommendation engine.
        Returns amount of water in mm and next expected irrigation.
        """
        amount = 0
        next_irrigation = "N/A"
        action = "No action needed"

        if moisture_stress in ['Moderate Stress', 'High Stress'] or ndmi < 0.2:
            action = "Irrigate Today"
            
            # Specific logic based on crop and growth stage
            if crop == 'Rice':
                if growth_stage in ['Vegetative', 'Flowering']:
                    amount = 45
                    next_irrigation = "3 days"
                else:
                    amount = 20
                    next_irrigation = "7 days"
            
            elif crop == 'Wheat':
                if growth_stage == 'Flowering':
                    amount = 40
                    next_irrigation = "5 days"
                else:
                    amount = 25
                    next_irrigation = "10 days"
            
            # Generic fallback for other crops
            else:
                amount = 30
                next_irrigation = "5 days"

        elif moisture_stress == 'Healthy':
            action = "Soil moisture optimal"
            amount = 0
            next_irrigation = "Check again in 7 days"

        return {
            'action': action,
            'amount_mm': amount,
            'next_irrigation': next_irrigation
        }
