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
