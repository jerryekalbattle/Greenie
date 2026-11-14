import os
import secrets


from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY environment variable is missing")


# Check whether the user has entered the correct API key
def verify_api_key(x_api_key: str = Header(default=None)):
    if not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    return True

app = FastAPI(
    title="Cardiovascular Surgeries (API)",
    description="IDK YET",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["X-API-Key", "Content-Type"]
)


@app.get("/verify-key", dependencies=[Depends(verify_api_key)])
def verify_key():
    return {
        "message": "API key verified successfully"
    }




@app.get("/")
def home():
    return {
        "message": "Welcome to the Cardiovascular Surgery API",
        "available_endpoints": [
            "GET /surgeries",
            "GET /surgeries/{surgery_id}"
        ]
    }


surgeries = {
    "0001": {
        "name": "Aortic Root Surgery",
        "category": "Aortic Surgery",
        "description": "A procedure involving the repair or replacement of the aortic root.",
        "medication_info": ["Medication information will be added here."],
        "surgery_info": {
            "Purpose": "Treat conditions affecting the aortic root.",
            "Procedure": "The surgeon repairs or replaces affected tissue."
        },
        "recovery": {
            "Overview": "Recovery varies by patient and surgical approach.",
            "Follow_up": "Follow the care team's instructions."
        },
        "risks": ["Bleeding", "Infection", "Blood clots"]
    }


}




# Return all surgery IDs and names
@app.get("/surgeries", dependencies=[Depends(verify_api_key)])
def get_surgeries():

    return [
        {
            "id": surgery_id,
            "name": surgery["name"],
            "category": surgery["category"],
            "description": surgery["description"]

        }
        for surgery_id, surgery in surgeries.items()
    ]


# Return detailed information using surgery ID
@app.get("/surgeries/{surgery_id}", dependencies=[Depends(verify_api_key)])
def get_surgery(surgery_id: str):

    if surgery_id not in surgeries:

        raise HTTPException(
            status_code=404,
            detail="Surgery ID not found"
        )

    return {
        "id": surgery_id,
        **surgeries[surgery_id]
    }
<<<<<<< HEAD



surgeries = {
    "aortic-root-surgery": {
        "name": "Aortic Root Surgery",
        "category": "Aortic Surgery",

        "description": "Educational overview of aortic root surgery.",

        "medication": {
            "information": "Medication depends on the patient's treatment plan."
        },

        "surgery_info": {
            "purpose": "Treat conditions affecting the aortic root.",
            "procedure": "The surgeon repairs or replaces affected tissue."
        },

        "recovery": {
            "overview": "Recovery varies by patient and surgical approach.",
            "follow_up": "Follow the care team's appointment schedule."
        },

        "risks": [
            "Bleeding",
            "Infection",
            "Blood clots"
        ]
    }
}
=======
>>>>>>> a20f98581e1de2706d276a4326d95d01f8bf54ee
