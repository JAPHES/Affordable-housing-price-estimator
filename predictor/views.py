from django.http import JsonResponse
from django.shortcuts import render

from .forms import PricePredictionForm
from .services import get_feature_names, predict_price


def format_kes(value):
    return f"KES {value:,.0f}"


def health(request):
    return JsonResponse({"status": "ok"})


def landing(request):
    return render(
        request,
        "predictor/landing.html",
        {
            "active_page": "home",
        },
    )


def predict(request):
    feature_names = get_feature_names()
    result = None
    submitted_values = None

    if request.method == "POST":
        form = PricePredictionForm(request.POST, feature_names=feature_names)
        if form.is_valid():
            submitted_values = form.feature_values()
            predicted_price = predict_price(submitted_values)
            result = {
                "raw": predicted_price,
                "formatted": format_kes(predicted_price),
            }
    else:
        form = PricePredictionForm(feature_names=feature_names)

    return render(
        request,
        "predictor/predict.html",
        {
            "form": form,
            "result": result,
            "submitted_values": submitted_values,
            "feature_count": len(feature_names),
            "active_page": "predict",
        },
    )
