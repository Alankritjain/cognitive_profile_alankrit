from math import erf, sqrt

class DigitSpanTest:
    """
    Class to represent a Digit Span Test (Forward & Backward).
    Handles scoring, z-score, percentile, and category classification.
    """

    # Fixed means and SDs for each age group
    AGE_GROUPS = {
        "10-13": {"mean": 7.1, "sd": 1.5},
        "14-16": {"mean": 7.9, "sd": 1.5},
        "17-18": {"mean": 8.0, "sd": 1.5},
    }

    CATEGORIES = [
        {"name": "Impaired", "min": 0, "max": 9},
        {"name": "Below Average", "min": 10, "max": 25},
        {"name": "Average", "min": 26, "max": 74},
        {"name": "Above Average", "min": 75, "max": 89},
        {"name": "Superior", "min": 90, "max": 100},
    ]

    def __init__(self, name, age, student_class, forward_raw, backward_raw):
        self.name = name
        self.age = age
        self.student_class = student_class
        self.forward_raw = forward_raw
        self.backward_raw = backward_raw

        # Get age group stats
        self.mean, self.sd = self._get_age_group_params(age)

        # Process results
        self.forward_z, self.forward_percentile, self.forward_category = self._process_score(forward_raw)
        self.backward_z, self.backward_percentile, self.backward_category = self._process_score(backward_raw)

    def _get_age_group_params(self, age):
        """Return mean and SD based on age group."""
        if 10 <= age <= 13:
            return self.AGE_GROUPS["10-13"]["mean"], self.AGE_GROUPS["10-13"]["sd"]
        elif 14 <= age <= 16:
            return self.AGE_GROUPS["14-16"]["mean"], self.AGE_GROUPS["14-16"]["sd"]
        elif 17 <= age <= 18:
            return self.AGE_GROUPS["17-18"]["mean"], self.AGE_GROUPS["17-18"]["sd"]
        else:
            raise ValueError("Age must be between 10 and 18.")

    def _z_score(self, raw):
        """Calculate z-score."""
        return round((raw - self.mean) / self.sd, 2)

    def _percentile(self, z):
        """
        Convert z-score to percentile using normal distribution.
        Formula: 0.5 * (1 + erf(z / sqrt(2)))
        """
        percentile = 0.5 * (1 + erf(z / sqrt(2)))
        return round(percentile * 100)

    def _category(self, percentile):
        """Assign category based on percentile range."""
        for cat in self.CATEGORIES:
            if cat["min"] <= percentile <= cat["max"]:
                return cat["name"]
        return "Unknown"

    def _process_score(self, raw):
        """Return z-score, percentile, and category for a given raw score."""
        z = self._z_score(raw)
        percentile = self._percentile(z)
        category = self._category(percentile)
        return z, percentile, category

    def to_dict(self):
        """Return results as dictionary for JSON rendering."""
        return {
            "name": self.name,
            "age": self.age,
            "class": self.student_class,
            "forward_raw_score": self.forward_raw,
            "forward_z_score": self.forward_z,
            "forward_percentile": self.forward_percentile,
            "forward_category": self.forward_category,
            "backward_raw_score": self.backward_raw,
            "backward_z_score": self.backward_z,
            "backward_percentile": self.backward_percentile,
            "backward_category": self.backward_category,
        }
