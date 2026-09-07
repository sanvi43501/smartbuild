from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import PlanningData, ConstructionProgress, CrackDetection
from ultralytics import YOLO
from PIL import Image
import os


# Load the crack detection AI model
MODEL_PATH = os.path.join(settings.BASE_DIR, "crack.pt")
model = YOLO(MODEL_PATH)


def home(request):
    return render(request, "home.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(email=email).first()

        if user:
            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                return redirect("dashboard")

        messages.error(request, "Invalid email or password.")

    return render(request, "login.html")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "dashboard.html")

def planning(request):

    planning_data = None
    location = None

    if request.method == "POST":

        location = request.POST.get("location")

        planning_data = PlanningData.objects.filter(
            location__iexact=location
        ).first()

    return render(
        request,
        "planning.html",
        {
            "location": location,
            "planning_data": planning_data,
        }
    )


def monitoring(request):

    project = ConstructionProgress.objects.last()

    if project:
        project_stage = project.project_stage
        current_status = project.current_status
        progress = project.progress
    else:
        project_stage = "Construction"
        current_status = "Work in Progress"
        progress = 70

    if request.method == "POST":

        project_stage = request.POST.get("project_stage")
        current_status = request.POST.get("current_status")
        progress = int(request.POST.get("progress"))

        ConstructionProgress.objects.create(
            project_stage=project_stage,
            current_status=current_status,
            progress=progress
        )

    milestones = [
        {
            "name": "Planning",
            "status": "completed"
        },
        {
            "name": "Site preparation",
            "status": "completed"
        },
        {
            "name": "Foundation",
            "status": "completed"
        },
        {
            "name": "Structural work",
            "status": "completed"
        },
        {
            "name": "Final inspection",
            "status": "pending"
        },
    ]

    return render(
        request,
        "monitoring.html",
        {
            "project_stage": project_stage,
            "current_status": current_status,
            "progress": progress,
            "milestones": milestones,
        }
    )


def maintenance(request):

    image_url = None
    result = None
    confidence = 0
    crack_count = 0
    severity = None
    recommendation = None

    if request.method == "POST" and request.FILES.get("building_image"):

        image = request.FILES["building_image"]

        # Save uploaded image
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)

        image_path = fs.path(filename)
        image_url = fs.url(filename)

        # Run AI crack detection
        predictions = model.predict(
            source=image_path,
            conf=0.25,
            verbose=False
        )

        prediction = predictions[0]

        # Check whether cracks were detected
        if prediction.boxes is not None and len(prediction.boxes) > 0:

            result = "🔴 Crack Detected"

            crack_count = len(prediction.boxes)

            confidence = float(
                prediction.boxes.conf.max().item()
            ) * 100

            confidence = round(confidence, 2)

            # Determine severity
            if crack_count >= 5 or confidence >= 85:
                severity = "🔴 High"

            elif crack_count >= 3 or confidence >= 60:
                severity = "🟠 Medium"

            else:
                severity = "🟡 Low"

            # Recommendation
            if severity == "🔴 High":

                recommendation = (
                    "Immediate professional inspection is recommended."
                )

            elif severity == "🟠 Medium":

                recommendation = (
                    "Further inspection and monitoring are recommended."
                )

            else:

                recommendation = (
                    "Continue monitoring the building condition."
                )

            # Create annotated image
            annotated_image = prediction.plot()

            annotated_filename = "analyzed_" + filename

            annotated_path = os.path.join(
                settings.MEDIA_ROOT,
                annotated_filename
            )

            Image.fromarray(annotated_image).save(
                annotated_path
            )

            image_url = settings.MEDIA_URL + annotated_filename

        else:

            result = "🟢 No Crack Detected"

            confidence = 0
            crack_count = 0
            severity = "🟢 None"

            recommendation = (
                "No visible cracks were detected. "
                "Continue regular building inspection."
            )

        # Save AI result to database
        CrackDetection.objects.create(
            image=filename,
            result=result,
            confidence=confidence,
            crack_count=crack_count,
            severity=severity,
            recommendation=recommendation
        )

    return render(
        request,
        "maintenance.html",
        {
            "image_url": image_url,
            "result": result,
            "confidence": confidence,
            "crack_count": crack_count,
            "severity": severity,
            "recommendation": recommendation,
        }
    )


def history(request):

    detections = CrackDetection.objects.all().order_by(
        "-detected_at"
    )

    return render(
        request,
        "history.html",
        {
            "detections": detections,
        }
    )


def report(request):

    # Latest planning information
    planning_data = PlanningData.objects.last()

    # Latest construction progress
    construction = ConstructionProgress.objects.last()

    # Latest AI crack detection
    crack_detection = CrackDetection.objects.order_by(
        "-detected_at"
    ).first()

    return render(
        request,
        "report.html",
        {
            "planning_data": planning_data,
            "construction": construction,
            "crack_detection": crack_detection,
        }
    )
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register.html")
def logout_view(request):
    logout(request)
    return redirect("home")