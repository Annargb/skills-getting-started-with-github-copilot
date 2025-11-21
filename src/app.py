from fastapi import FastAPI, HTTPException, status, Query, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
import os
from src.activities_db import activities as global_activities

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# Dependency для доступа к activities


def get_activities():
    return global_activities


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities_endpoint(activities=Depends(get_activities)):
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, activities=Depends(get_activities)):
    """Sign up a student for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str = Query(...), activities=Depends(get_activities)):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail=f"Activity not found: {activity_name}")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=404,
            detail=f"Student '{email}' not found in activity '{activity_name}'. Current participants: {activity['participants']}"
        )
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
