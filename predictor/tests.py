from django.test import SimpleTestCase
from django.urls import reverse

from .forms import FIELD_CONFIG
from .services import get_feature_names


class PredictorViewTests(SimpleTestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse("predictor:health"), secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_landing_page_uses_root_relative_static_assets(self):
        response = self.client.get(reverse("predictor:landing"), secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/static/predictor/styles")
        self.assertContains(response, "/static/predictor/hero-housing")

    def test_prediction_page_loads_model_inputs(self):
        response = self.client.get(reverse("predictor:predict"), secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["feature_count"], len(get_feature_names()))
        self.assertContains(response, "Property and finance details")
        self.assertContains(response, "About this estimate")
        self.assertContains(response, "not a formal property valuation")

    def test_prediction_form_provides_defaults_and_guidance(self):
        response = self.client.get(reverse("predictor:predict"), secure=True)
        form = response.context["form"]

        self.assertEqual(
            [section["name"] for section in form.grouped_sections()],
            ["Project Costs", "Property", "Financing", "Buyer Profile"],
        )
        for name in get_feature_names():
            self.assertEqual(form[name].value(), FIELD_CONFIG[name]["initial"])
            self.assertEqual(form[name].help_text, FIELD_CONFIG[name]["help"])

        self.assertContains(response, "Accepted range: KES 118,400–1,647,900")

    def test_invalid_prediction_submission_shows_validation_summary(self):
        form_data = {
            name: FIELD_CONFIG[name]["initial"]
            for name in get_feature_names()
        }
        form_data["financing_cost_ksh"] = 0

        response = self.client.post(
            reverse("predictor:predict"),
            data=form_data,
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertContains(response, "Some values need your attention.")
        self.assertContains(response, "Check the highlighted fields")

    def test_prediction_submission_returns_a_non_negative_price(self):
        feature_names = get_feature_names()
        form_data = {
            name: FIELD_CONFIG.get(name, {}).get("initial", 0)
            for name in feature_names
        }

        response = self.client.post(
            reverse("predictor:predict"),
            data=form_data,
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].errors)
        self.assertGreaterEqual(response.context["result"]["raw"], 0)
        self.assertContains(response, response.context["result"]["formatted"])
        self.assertContains(response, "Calculated from the values currently entered.")
