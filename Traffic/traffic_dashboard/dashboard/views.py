import os
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "traffic_analysis"
COLLECTION_NAME = "cleaned_traffic"


def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME], client


def aggregate_mongo(filters=None):
    collection, client = get_mongo_collection()
    match_stage = {}
    if filters:
        if "date" in filters and filters["date"]:
            match_stage["Date"] = filters["date"]
        if "location" in filters and filters["location"]:
            match_stage["Location"] = filters["location"]

    pipeline = []
    if match_stage:
        pipeline.append({"$match": match_stage})

    pipeline.extend([
        {
            "$group": {
                "_id": "$Hour",
                "total_vehicles": {"$sum": "$Vehicle Count"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
    ])

    hourly = list(collection.aggregate(pipeline))
    location_pipeline = [{"$group": {"_id": "$Location", "total_vehicles": {"$sum": "$Vehicle Count"}}}, {"$sort": {"total_vehicles": -1}}]
    type_pipeline = [{"$group": {"_id": "$Vehicle Type", "total_vehicles": {"$sum": "$Vehicle Count"}}}, {"$sort": {"total_vehicles": -1}}]
    location_data = list(collection.aggregate(location_pipeline))
    vehicle_type_data = list(collection.aggregate(type_pipeline))
    client.close()

    return hourly, location_data, vehicle_type_data


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "dashboard/login.html", {"error": "Invalid username or password."})
    return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard_view(request):
    date_filter = request.GET.get("date", "")
    location_filter = request.GET.get("location", "")
    filters = {"date": date_filter, "location": location_filter}

    hourly, location_data, vehicle_type_data = aggregate_mongo(filters)
    context = {
        "hourly": hourly,
        "locations": location_data,
        "types": vehicle_type_data,
        "selected_date": date_filter,
        "selected_location": location_filter,
    }
    return render(request, "dashboard/dashboard.html", context)
