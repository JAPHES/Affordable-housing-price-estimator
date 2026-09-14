from django import forms


GROUP_CONFIG = {
    "Project Costs": "Enter the main cost components used to develop or purchase the home.",
    "Property": "Describe the size of the home and its cost per square metre.",
    "Financing": "Provide the expected repayment and annual interest rate.",
    "Buyer Profile": "Add the buyer's monthly income and housing levy contribution.",
}


def example_placeholder(value):
    if value is None:
        return ""
    if isinstance(value, float) and not value.is_integer():
        formatted_value = f"{value:g}"
    else:
        formatted_value = f"{value:,.0f}"
    return f"e.g. {formatted_value}"


FIELD_CONFIG = {
    "financing_cost_ksh": {
        "label": "Financing cost",
        "min": 118400,
        "max": 1647900,
        "example": 440100,
        "step": 1000,
        "prefix": "KES",
        "group": "Project Costs",
        "help": "Total financing charges associated with the purchase.",
        "range": "Accepted range: KES 118,400–1,647,900",
    },
    "construction_cost_ksh": {
        "label": "Construction cost",
        "min": 591800,
        "max": 8239300,
        "example": 2200450,
        "step": 5000,
        "prefix": "KES",
        "group": "Project Costs",
        "help": "Estimated cost of materials, labour, and delivery.",
        "range": "Accepted range: KES 591,800–8,239,300",
    },
    "markup_ksh": {
        "label": "Markup",
        "min": 66800,
        "max": 1977400,
        "example": 343250,
        "step": 1000,
        "prefix": "KES",
        "group": "Project Costs",
        "help": "Developer or seller margin included in the final price.",
        "range": "Accepted range: KES 66,800–1,977,400",
    },
    "size_sqm": {
        "label": "House size",
        "min": 17,
        "max": 83,
        "example": 52,
        "step": 1,
        "suffix": "sqm",
        "group": "Property",
        "help": "Internal floor area of the home.",
        "range": "Accepted range: 17–83 sqm",
    },
    "cost_per_sqm_ksh": {
        "label": "Cost per square metre",
        "min": 32022,
        "max": 105759,
        "example": 50146,
        "step": 500,
        "prefix": "KES",
        "group": "Property",
        "help": "Average construction or purchase cost per square metre.",
        "range": "Accepted range: KES 32,022–105,759",
    },
    "monthly_repayment_ksh": {
        "label": "Monthly repayment",
        "min": 2980,
        "max": 107950,
        "example": 17785,
        "step": 500,
        "prefix": "KES",
        "group": "Financing",
        "help": "Expected monthly loan or mortgage repayment.",
        "range": "Accepted range: KES 2,980–107,950",
    },
    "interest_rate_pct": {
        "label": "Interest rate",
        "min": 3,
        "max": 9,
        "example": 6,
        "step": 0.1,
        "suffix": "%",
        "group": "Financing",
        "help": "Annual interest rate for the housing finance facility.",
        "range": "Accepted range: 3–9%",
    },
    "housing_levy_contribution_ksh": {
        "label": "Housing levy contribution",
        "min": 150,
        "max": 7440,
        "example": 1065,
        "step": 50,
        "prefix": "KES",
        "group": "Buyer Profile",
        "help": "Buyer's expected monthly housing levy contribution.",
        "range": "Accepted range: KES 150–7,440",
    },
    "buyer_monthly_income_ksh": {
        "label": "Buyer monthly income",
        "min": 10000,
        "max": 496000,
        "example": 71200,
        "step": 1000,
        "prefix": "KES",
        "group": "Buyer Profile",
        "help": "Buyer's gross monthly income before deductions.",
        "range": "Accepted range: KES 10,000–496,000",
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
                "placeholder": example_placeholder(config.get("example")),
            }
            if min_value is not None:
                attrs["min"] = min_value
            if max_value is not None:
                attrs["max"] = max_value

            self.fields[name] = forms.FloatField(
                label=config.get("label", name.replace("_", " ").title()),
                min_value=min_value,
                max_value=max_value,
                help_text=config.get("help", ""),
                widget=forms.NumberInput(attrs=attrs),
            )

    def grouped_sections(self):
        groups = {}
        for name in self.feature_names:
            config = FIELD_CONFIG.get(name, {})
            group = config.get("group", "Model Inputs")
            groups.setdefault(group, []).append(
                {
                    "field": self[name],
                    "prefix": config.get("prefix", ""),
                    "suffix": config.get("suffix", ""),
                    "range": config.get("range", ""),
                }
            )

        group_names = list(GROUP_CONFIG)
        group_names += [name for name in groups if name not in GROUP_CONFIG]
        return [
            {
                "name": name,
                "description": GROUP_CONFIG.get(name, "Provide the values used by the model."),
                "controls": groups[name],
            }
            for name in group_names
            if name in groups
        ]

    def feature_values(self):
        return {name: self.cleaned_data[name] for name in self.feature_names}
