from django import forms


FIELD_CONFIG = {
    "financing_cost_ksh": {
        "label": "Financing cost",
        "min": 118400,
        "max": 1647900,
        "initial": 440100,
        "step": 1000,
        "prefix": "KES",
        "group": "Project Costs",
    },
    "construction_cost_ksh": {
        "label": "Construction cost",
        "min": 591800,
        "max": 8239300,
        "initial": 2200450,
        "step": 5000,
        "prefix": "KES",
        "group": "Project Costs",
    },
    "markup_ksh": {
        "label": "Markup",
        "min": 66800,
        "max": 1977400,
        "initial": 343250,
        "step": 1000,
        "prefix": "KES",
        "group": "Project Costs",
    },
    "size_sqm": {
        "label": "House size",
        "min": 17,
        "max": 83,
        "initial": 52,
        "step": 1,
        "suffix": "sqm",
        "group": "Property",
    },
    "cost_per_sqm_ksh": {
        "label": "Cost per square metre",
        "min": 32022,
        "max": 105759,
        "initial": 50146,
        "step": 500,
        "prefix": "KES",
        "group": "Property",
    },
    "monthly_repayment_ksh": {
        "label": "Monthly repayment",
        "min": 2980,
        "max": 107950,
        "initial": 17785,
        "step": 500,
        "prefix": "KES",
        "group": "Financing",
    },
    "interest_rate_pct": {
        "label": "Interest rate",
        "min": 3,
        "max": 9,
        "initial": 6,
        "step": 0.1,
        "suffix": "%",
        "group": "Financing",
    },
    "housing_levy_contribution_ksh": {
        "label": "Housing levy contribution",
        "min": 150,
        "max": 7440,
        "initial": 1065,
        "step": 50,
        "prefix": "KES",
        "group": "Buyer Profile",
    },
    "buyer_monthly_income_ksh": {
        "label": "Buyer monthly income",
        "min": 10000,
        "max": 496000,
        "initial": 71200,
        "step": 1000,
        "prefix": "KES",
        "group": "Buyer Profile",
    },
}


class PricePredictionForm(forms.Form):
    def __init__(self, *args, feature_names=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.feature_names = list(feature_names or FIELD_CONFIG.keys())

        for name in self.feature_names:
            config = FIELD_CONFIG.get(name, {})
            min_value = config.get("min", 0)
            max_value = config.get("max")
            step = config.get("step", 1)
            attrs = {
                "class": "control-input",
                "inputmode": "decimal",
                "step": step,
            }
            if min_value is not None:
                attrs["min"] = min_value
            if max_value is not None:
                attrs["max"] = max_value

            self.fields[name] = forms.FloatField(
                label=config.get("label", name.replace("_", " ").title()),
                min_value=min_value,
                max_value=max_value,
                widget=forms.NumberInput(attrs=attrs),
            )

    def grouped_fields(self):
        groups = {}
        for name in self.feature_names:
            config = FIELD_CONFIG.get(name, {})
            group = config.get("group", "Model Inputs")
            groups.setdefault(group, []).append(
                {
                    "field": self[name],
                    "prefix": config.get("prefix", ""),
                    "suffix": config.get("suffix", ""),
                }
            )
        return groups.items()

    def feature_values(self):
        return {name: self.cleaned_data[name] for name in self.feature_names}
