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
        "http://127.0.0.1:5173",
        "https://greenie-nine.vercel.app"
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
    "aortic-root-surgery": {
        "name": "aortic root surgery",
        "category": "aortic surgery",
        "description": "an educational overview of aortic root surgery.",
        "medication": {
            "information": "medication may include beta blockers, blood pressure medications, anticoagulants, and pain relievers depending on the patient's treatment plan."
        },
        "surgery_info": {
            "purpose": "treats an enlarged, damaged, or weakened aortic root, including aortic aneurysms.",
            "procedure": "the surgeon removes the damaged aortic root and replaces it with a synthetic graft. the aortic valve may also be repaired or replaced."
        },
        "recovery": {
            "overview": "recovery includes hospital monitoring, pain management, incision care, breathing exercises, and gradual physical activity.",
            "follow_up": "follow-up includes cardiology appointments, imaging, blood pressure monitoring, and evaluation of the repaired aorta and valve."
        },
        "risks": ["bleeding", "infection", "stroke", "irregular heartbeat", "kidney injury", "blood clots", "graft complications"]
    },

    "aortic-valve-repair-and-replacement": {
        "name": "aortic valve repair and replacement",
        "category": "heart valve surgery",
        "description": "an educational overview of aortic valve repair and replacement.",
        "medication": {
            "information": "medication may include anticoagulants, antiplatelet medications, beta blockers, diuretics, and pain relievers depending on the type of valve treatment."
        },
        "surgery_info": {
            "purpose": "treats aortic stenosis, aortic regurgitation, and other conditions affecting the aortic valve.",
            "procedure": "the surgeon repairs the damaged valve or removes it and replaces it with a mechanical or biological valve."
        },
        "recovery": {
            "overview": "recovery includes heart monitoring, pain management, incision care, breathing exercises, and gradually increasing physical activity.",
            "follow_up": "follow-up includes echocardiograms, cardiology appointments, and valve-function monitoring."
        },
        "risks": ["bleeding", "infection", "stroke", "blood clots", "irregular heartbeat", "valve leakage", "prosthetic valve failure"]
    },

    "atrial-fibrillation-ablation": {
        "name": "atrial fibrillation ablation",
        "category": "cardiac electrophysiology",
        "description": "an educational overview of atrial fibrillation ablation.",
        "medication": {
            "information": "medication may include anticoagulants, beta blockers, and antiarrhythmic medications to manage heart rhythm and reduce blood clot risk."
        },
        "surgery_info": {
            "purpose": "treats atrial fibrillation, an irregular heart rhythm originating in the upper chambers of the heart.",
            "procedure": "the surgeon guides catheters through blood vessels into the heart. electrical mapping identifies abnormal signals, and specialized energy is used to isolate the tissue responsible for the irregular rhythm."
        },
        "recovery": {
            "overview": "patients are monitored for several hours or overnight. recovery includes checking the catheter insertion site and monitoring heart rhythm.",
            "follow_up": "follow-up includes ecgs, heart rhythm monitoring, and cardiology appointments."
        },
        "risks": ["bleeding", "blood vessel damage", "stroke", "cardiac perforation", "pulmonary vein narrowing", "heart rhythm recurrence", "damage to nearby structures"]
    },

    "atrial-flutter-ablation": {
        "name": "atrial flutter ablation",
        "category": "cardiac electrophysiology",
        "description": "an educational overview of atrial flutter ablation.",
        "medication": {
            "information": "medication may include anticoagulants, beta blockers, and medications that control heart rate and reduce blood clot risk."
        },
        "surgery_info": {
            "purpose": "treats atrial flutter, an abnormal heart rhythm that causes the upper chambers of the heart to beat rapidly.",
            "procedure": "the surgeon guides catheters through blood vessels into the heart. electrical mapping identifies the abnormal circuit, and radiofrequency energy interrupts the electrical pathway."
        },
        "recovery": {
            "overview": "most patients are monitored for several hours and may return home the same day. recovery includes checking the catheter insertion site and temporarily limiting strenuous activity.",
            "follow_up": "follow-up includes ecgs, heart rhythm monitoring, and cardiology appointments."
        },
        "risks": ["bleeding", "infection", "blood vessel damage", "stroke", "cardiac perforation", "heart block", "arrhythmia recurrence"]
    },

    "cardiac-ablation": {
        "name": "cardiac ablation",
        "category": "cardiac electrophysiology",
        "description": "an educational overview of cardiac ablation.",
        "medication": {
            "information": "medication may include beta blockers, antiarrhythmic medications, and anticoagulants depending on the heart rhythm condition being treated."
        },
        "surgery_info": {
            "purpose": "treats abnormal heart rhythms such as supraventricular tachycardia, atrial fibrillation, atrial flutter, and certain ventricular tachycardias.",
            "procedure": "the surgeon guides catheters through blood vessels into the heart. electrical mapping identifies abnormal tissue, and specialized energy interrupts the electrical pathways causing the arrhythmia."
        },
        "recovery": {
            "overview": "patients are monitored for several hours or overnight. recovery includes observation of heart rhythm and catheter insertion sites.",
            "follow_up": "follow-up includes ecgs, heart monitors, and cardiology appointments."
        },
        "risks": ["bleeding", "infection", "blood clots", "stroke", "cardiac perforation", "blood vessel damage", "damage to the heart's electrical system"]
    },

    "cardiac-rehabilitation": {
        "name": "cardiac rehabilitation",
        "category": "cardiovascular rehabilitation",
        "description": "an educational overview of cardiac rehabilitation.",
        "medication": {
            "information": "medication may include cholesterol-lowering medications, blood pressure medications, antiplatelet medications, and medications that support heart function."
        },
        "surgery_info": {
            "purpose": "improves physical fitness, cardiovascular health, and quality of life after heart attacks, heart surgery, or other cardiovascular conditions.",
            "procedure": "patients participate in medically supervised exercise sessions, health education, and lifestyle counseling. medical professionals monitor heart rate, blood pressure, and physical activity."
        },
        "recovery": {
            "overview": "patients gradually improve endurance, strength, and exercise tolerance through supervised exercise and independent activities.",
            "follow_up": "continued exercise, heart-healthy nutrition, stress management, medication adherence, and regular medical appointments are encouraged."
        },
        "risks": ["exercise-related chest pain", "abnormal heart rhythms", "dizziness", "shortness of breath", "blood pressure changes"]
    },

    "cardiac-resynchronization-therapy": {
        "name": "cardiac resynchronization therapy",
        "category": "cardiac device implantation",
        "description": "an educational overview of cardiac resynchronization therapy.",
        "medication": {
            "information": "medication may include heart failure medications, beta blockers, diuretics, and medications that help manage blood pressure and fluid retention."
        },
        "surgery_info": {
            "purpose": "treats selected patients with heart failure whose ventricles do not contract together efficiently.",
            "procedure": "the surgeon makes an incision below the collarbone and guides electrical leads through a vein into the heart. the leads connect to an implanted pulse generator that coordinates heart contractions."
        },
        "recovery": {
            "overview": "patients may stay overnight for monitoring. recovery includes incision care, device testing, and temporary restrictions on heavy lifting and certain arm movements.",
            "follow_up": "follow-up includes device checks, cardiology appointments, and remote monitoring."
        },
        "risks": ["infection", "bleeding", "lead displacement", "blood vessel damage", "pneumothorax", "device malfunction"]
    },

    "cardiovascular-disease-prevention": {
        "name": "cardiovascular disease prevention",
        "category": "preventive cardiology",
        "description": "an educational overview of cardiovascular disease prevention.",
        "medication": {
            "information": "medication may include cholesterol-lowering medications, blood pressure medications, and medications that help manage diabetes and reduce cardiovascular risk."
        },
        "surgery_info": {
            "purpose": "reduces the risk of heart attacks, strokes, coronary artery disease, and other cardiovascular conditions.",
            "procedure": "healthcare professionals evaluate blood pressure, cholesterol, blood glucose, family history, smoking habits, diet, and physical activity. patients receive individualized recommendations involving nutrition, exercise, screening, and medication when appropriate."
        },
        "recovery": {
            "overview": "preventive care is ongoing rather than a one-time recovery process. patients work toward healthier habits and management of cardiovascular risk factors.",
            "follow_up": "regular primary care and cardiology appointments, blood pressure checks, cholesterol testing, and diabetes screening may be recommended."
        },
        "risks": ["untreated high blood pressure", "heart attack", "stroke", "heart failure", "kidney damage", "peripheral artery disease"]
    },

    "carotid-angioplasty-and-stenting": {
        "name": "carotid angioplasty and stenting",
        "category": "vascular surgery",
        "description": "an educational overview of carotid angioplasty and stenting.",
        "medication": {
            "information": "medication may include antiplatelet medications, cholesterol-lowering medications, and blood pressure medications to reduce the risk of complications."
        },
        "surgery_info": {
            "purpose": "treats carotid artery narrowing caused by plaque buildup and helps reduce the risk of stroke in appropriately selected patients.",
            "procedure": "the surgeon guides a catheter through an artery to the narrowed carotid artery. a balloon expands the narrowed area, and a small metal mesh stent helps keep the artery open."
        },
        "recovery": {
            "overview": "patients receive blood pressure and neurological monitoring, often staying overnight. recovery includes checking the catheter insertion site and limiting strenuous activity.",
            "follow_up": "follow-up includes neurological assessments, carotid ultrasound imaging, blood pressure monitoring, and cholesterol management."
        },
        "risks": ["stroke", "bleeding", "blood vessel damage", "blood clots", "restenosis", "kidney injury from contrast dye"]
    },

    "carotid-endarterectomy": {
        "name": "carotid endarterectomy",
        "category": "vascular surgery",
        "description": "an educational overview of carotid endarterectomy.",
        "medication": {
            "information": "medication may include antiplatelet medications, cholesterol-lowering medications, and blood pressure medications depending on the patient's condition."
        },
        "surgery_info": {
            "purpose": "treats significant carotid artery narrowing caused by plaque buildup and reduces the risk of stroke in selected patients.",
            "procedure": "the surgeon makes an incision in the neck to access the carotid artery. the artery is opened, cleared of plaque buildup, and closed with sutures or a patch."
        },
        "recovery": {
            "overview": "patients are commonly monitored in the hospital for approximately one day. recovery includes neurological assessments, blood pressure monitoring, and incision care.",
            "follow_up": "follow-up includes carotid ultrasound examinations, blood pressure monitoring, cholesterol management, and vascular specialist appointments."
        },
        "risks": ["stroke", "heart attack", "bleeding", "neck hematoma", "cranial nerve injury", "infection", "restenosis"]
    },

    "coronary-artery-bypass-grafting": {
        "name": "coronary artery bypass grafting",
        "category": "coronary artery surgery",
        "description": "an educational overview of coronary artery bypass grafting.",
        "medication": {
            "information": "medication may include antiplatelet medications, cholesterol-lowering medications, beta blockers, blood pressure medications, diuretics, and pain relievers."
        },
        "surgery_info": {
            "purpose": "treats coronary artery disease when narrowed or blocked arteries restrict blood flow to the heart muscle.",
            "procedure": "the surgeon collects a healthy blood vessel from the chest, arm, or leg and attaches it to the coronary artery beyond the blockage to create an alternate pathway for blood flow."
        },
        "recovery": {
            "overview": "recovery includes hospital monitoring, incision care, pain management, breathing exercises, and gradually increasing physical activity.",
            "follow_up": "follow-up includes cardiac rehabilitation, cardiology appointments, medication management, and cholesterol monitoring."
        },
        "risks": ["bleeding", "infection", "heart attack", "stroke", "irregular heartbeat", "kidney injury", "graft failure"]
    },

    "extracorporeal-membrane-oxygenation": {
        "name": "extracorporeal membrane oxygenation (ecmo)",
        "category": "mechanical circulatory support",
        "description": "an educational overview of extracorporeal membrane oxygenation.",
        "medication": {
            "information": "medication may include anticoagulants, sedatives, pain relievers, blood pressure support medications, and antibiotics."
        },
        "surgery_info": {
            "purpose": "provides temporary heart and/or lung support when a patient cannot maintain adequate circulation or oxygenation independently.",
            "procedure": "large tubes called cannulas are inserted into major blood vessels. blood travels through an external machine that adds oxygen, removes carbon dioxide, and pumps blood back into the patient."
        },
        "recovery": {
            "overview": "patients require intensive care and continuous monitoring of oxygen levels, circulation, bleeding, clotting, and organ function.",
            "follow_up": "follow-up includes treatment of the original heart or lung condition, rehabilitation, and monitoring for complications."
        },
        "risks": ["severe bleeding", "blood clots", "stroke", "infection", "kidney injury", "hemolysis", "limb ischemia"]
    },

    "general-anesthesia": {
        "name": "general anesthesia",
        "category": "anesthesia",
        "description": "an educational overview of general anesthesia.",
        "medication": {
            "information": "medication may include anesthetics, pain relievers, muscle relaxants, and medications to prevent nausea and vomiting."
        },
        "surgery_info": {
            "purpose": "prevents awareness and pain during major surgical procedures while allowing medical professionals to control breathing and monitor vital functions.",
            "procedure": "an anesthesiologist administers medications through an iv or inhaled gases to produce unconsciousness. a breathing tube may be inserted while medical equipment monitors vital signs."
        },
        "recovery": {
            "overview": "patients are transferred to a recovery unit where medical staff monitor breathing, oxygen levels, blood pressure, pain, nausea, and alertness.",
            "follow_up": "patients receive instructions regarding driving, eating, drinking, activity, and medication use."
        },
        "risks": ["nausea", "vomiting", "sore throat", "temporary confusion", "breathing complications", "blood pressure changes", "allergic reactions"]
    },

    "heart-cardiac-catheterization": {
        "name": "heart (cardiac) catheterization",
        "category": "cardiac diagnostic procedures",
        "description": "an educational overview of heart catheterization.",
        "medication": {
            "information": "medication may include anticoagulants, antiplatelet medications, sedatives, and medications used to manage chest pain."
        },
        "surgery_info": {
            "purpose": "diagnoses coronary artery disease, evaluates heart function, measures heart pressures, and may help treat narrowed blood vessels.",
            "procedure": "a catheter is inserted through an artery or vein, commonly in the wrist or groin, and guided toward the heart. contrast dye and x-ray imaging may be used to examine blood vessels."
        },
        "recovery": {
            "overview": "patients are monitored for several hours. medical staff check the insertion site, blood pressure, and heart rhythm. many patients return home the same day.",
            "follow_up": "follow-up includes reviewing test results, checking kidney function when indicated, and arranging additional cardiology treatment if needed."
        },
        "risks": ["bleeding", "infection", "blood vessel damage", "abnormal heart rhythms", "kidney injury", "allergic reaction to contrast dye", "stroke"]
    },

    "heart-transplant": {
        "name": "heart transplant",
        "category": "transplant surgery",
        "description": "an educational overview of heart transplantation.",
        "medication": {
            "information": "medication may include immunosuppressants to prevent organ rejection, antibiotics, antiviral medications, and antifungal medications to reduce infection risk."
        },
        "surgery_info": {
            "purpose": "treats advanced heart failure when other medical and surgical treatments are no longer sufficient.",
            "procedure": "the surgeon removes the diseased heart and positions a healthy donor heart in the chest. the major blood vessels are connected to restore blood circulation."
        },
        "recovery": {
            "overview": "patients spend time in a transplant intensive care unit and receive close monitoring for infection, organ rejection, bleeding, and kidney problems.",
            "follow_up": "lifelong transplant team appointments, heart-function testing, biopsies when indicated, and immunosuppressant therapy are required."
        },
        "risks": ["organ rejection", "infection", "bleeding", "kidney injury", "coronary allograft vasculopathy", "medication complications"]
    },

    "heart-valve-surgery": {
        "name": "heart valve surgery",
        "category": "heart valve surgery",
        "description": "an educational overview of heart valve surgery.",
        "medication": {
            "information": "medication may include anticoagulants, antiplatelet medications, beta blockers, diuretics, and pain relievers depending on the valve condition and treatment."
        },
        "surgery_info": {
            "purpose": "treats heart valve diseases such as stenosis, regurgitation, and other structural valve abnormalities.",
            "procedure": "the surgeon accesses the heart through a surgical incision and repairs or replaces the damaged valve. replacement valves may be mechanical or biological."
        },
        "recovery": {
            "overview": "patients may require intensive care monitoring, pain management, incision care, and gradual physical activity.",
            "follow_up": "follow-up includes echocardiograms, cardiology appointments, valve-function monitoring, and medication management."
        },
        "risks": ["bleeding", "infection", "stroke", "blood clots", "irregular heartbeat", "valve dysfunction"]
    },

    "implantable-cardioverter-defibrillator": {
        "name": "implantable cardioverter-defibrillator (icd)",
        "category": "cardiac device implantation",
        "description": "an educational overview of an implantable cardioverter-defibrillator.",
        "medication": {
            "information": "medication may include beta blockers, antiarrhythmic medications, anticoagulants when indicated, and pain relievers following implantation."
        },
        "surgery_info": {
            "purpose": "helps prevent sudden cardiac death in patients at risk of dangerous ventricular arrhythmias.",
            "procedure": "the surgeon makes an incision below the collarbone and guides electrical leads through a vein into the heart. the leads connect to a generator implanted beneath the skin that detects dangerous rhythms and delivers electrical treatment when necessary."
        },
        "recovery": {
            "overview": "patients are monitored for device function and complications. recovery includes incision care and temporary restrictions on heavy lifting and certain arm movements.",
            "follow_up": "follow-up includes regular device checks, remote monitoring, wound examinations, and cardiology appointments."
        },
        "risks": ["infection", "bleeding", "lead displacement", "pneumothorax", "device malfunction", "inappropriate electrical shocks"]
    },

    "intra-aortic-balloon-pump": {
        "name": "intra-aortic balloon pump (iabp)",
        "category": "mechanical circulatory support",
        "description": "an educational overview of an intra-aortic balloon pump.",
        "medication": {
            "information": "medication may include anticoagulants, blood pressure support medications, and medications that support heart function."
        },
        "surgery_info": {
            "purpose": "temporarily supports circulation in patients with severe heart dysfunction or certain complications following cardiac procedures.",
            "procedure": "a catheter containing a balloon is inserted into an artery and positioned in the descending aorta. the balloon inflates and deflates in coordination with the heartbeat to improve blood flow and reduce the heart's workload."
        },
        "recovery": {
            "overview": "patients require intensive care monitoring of blood pressure, heart function, circulation, and the catheter insertion site. movement may be restricted while the device remains in place.",
            "follow_up": "the device is removed when circulation improves or another treatment becomes available. the underlying heart condition requires continued treatment and monitoring."
        },
        "risks": ["bleeding", "blood clots", "limb ischemia", "vascular injury", "infection", "balloon malfunction"]
    },

    "lung-transplant": {
        "name": "lung transplant",
        "category": "transplant surgery",
        "description": "an educational overview of lung transplantation.",
        "medication": {
            "information": "medication may include immunosuppressants, antibiotics, antiviral medications, and antifungal medications to prevent organ rejection and reduce infection risk."
        },
        "surgery_info": {
            "purpose": "treats severe lung diseases when other available treatments are no longer sufficient.",
            "procedure": "the surgeon removes one or both diseased lungs and positions healthy donor lungs. the airways and blood vessels are connected to restore breathing function."
        },
        "recovery": {
            "overview": "patients receive intensive care, respiratory support, and close monitoring of oxygen levels and lung function. recovery includes respiratory therapy and physical rehabilitation.",
            "follow_up": "follow-up includes transplant appointments, lung-function testing, imaging, and immunosuppressant medication monitoring."
        },
        "risks": ["organ rejection", "infection", "bleeding", "airway complications", "blood clots", "primary graft dysfunction"]
    },

    "lung-volume-reduction-surgery": {
        "name": "lung volume reduction surgery",
        "category": "thoracic surgery",
        "description": "an educational overview of lung volume reduction surgery.",
        "medication": {
            "information": "medication may include bronchodilators, inhaled corticosteroids, medications to manage respiratory symptoms, and pain relievers following surgery."
        },
        "surgery_info": {
            "purpose": "improves lung function and breathing in selected patients with severe emphysema by removing nonfunctional portions of the lungs.",
            "procedure": "the surgeon accesses the chest through an open or minimally invasive approach and removes severely damaged lung tissue. this allows healthier portions of the lungs to expand and function more efficiently."
        },
        "recovery": {
            "overview": "patients may remain hospitalized for several days. recovery includes chest tube management, breathing exercises, oxygen monitoring, and pulmonary rehabilitation.",
            "follow_up": "follow-up includes pulmonary function testing, imaging, respiratory therapy, and monitoring for complications such as air leaks."
        },
        "risks": ["air leaks", "pneumonia", "bleeding", "infection", "respiratory failure", "blood clots"]
    },
    "maze-procedure": {
        "name": "maze procedure",
        "category": "cardiac arrhythmia surgery",
        "description": "an educational overview of the maze procedure.",
        "medication": {
            "information": "medication may include anticoagulants, beta blockers, antiarrhythmic medications, and pain relievers depending on the patient's condition."
        },
        "surgery_info": {
            "purpose": "treats atrial fibrillation by creating a pattern of scar tissue that directs electrical signals through normal pathways.",
            "procedure": "the surgeon accesses the heart and creates controlled lines of scar tissue using surgical incisions or energy-based techniques. these lines interrupt abnormal electrical pathways responsible for atrial fibrillation."
        },
        "recovery": {
            "overview": "recovery includes hospital monitoring, pain management, incision care, heart rhythm observation, and gradual physical rehabilitation.",
            "follow_up": "follow-up includes ecgs, heart rhythm monitoring, and cardiology appointments. anticoagulation decisions depend on individual stroke risk."
        },
        "risks": ["bleeding", "infection", "stroke", "heart block", "need for a pacemaker", "irregular heartbeat recurrence"]
    },

    "minimally-invasive-heart-surgery": {
        "name": "minimally invasive heart surgery",
        "category": "minimally invasive cardiac surgery",
        "description": "an educational overview of minimally invasive heart surgery.",
        "medication": {
            "information": "medication may include pain relievers, antiplatelet medications, beta blockers, diuretics, and antibiotics depending on the procedure."
        },
        "surgery_info": {
            "purpose": "allows surgeons to treat selected cardiovascular conditions while potentially reducing surgical trauma and recovery time.",
            "procedure": "the surgeon makes smaller incisions between the ribs or in another appropriate location. specialized instruments and cameras are used to access the heart and repair or replace the affected structure."
        },
        "recovery": {
            "overview": "recovery may involve less discomfort and a shorter hospital stay than traditional open surgery, depending on the operation. patients still require heart monitoring, incision care, and gradual activity progression.",
            "follow_up": "follow-up includes cardiology appointments, imaging, wound evaluation, and rehabilitation when appropriate."
        },
        "risks": ["bleeding", "infection", "blood vessel injury", "irregular heartbeat", "conversion to open surgery", "organ complications"]
    },

    "minimally-invasive-surgery": {
        "name": "minimally invasive surgery",
        "category": "surgical techniques",
        "description": "an educational overview of minimally invasive surgery.",
        "medication": {
            "information": "medication may include anesthetics, pain relievers, antibiotics, and anticoagulants depending on the procedure and patient's condition."
        },
        "surgery_info": {
            "purpose": "treats various medical conditions while potentially reducing incision size, tissue damage, and recovery time.",
            "procedure": "the surgeon makes small incisions and inserts specialized instruments, cameras, or scopes. the operation is performed using direct visualization or video guidance, depending on the condition being treated."
        },
        "recovery": {
            "overview": "recovery varies depending on the procedure. patients may experience less postoperative discomfort and shorter hospital stays than with some traditional operations.",
            "follow_up": "follow-up includes wound care, activity restrictions, evaluation of surgical results, and specialist appointments."
        },
        "risks": ["bleeding", "infection", "organ injury", "anesthesia complications", "conversion to open surgery", "blood clots"]
    },

    "mitral-valve-repair-and-replacement": {
        "name": "mitral valve repair and replacement",
        "category": "heart valve surgery",
        "description": "an educational overview of mitral valve repair and replacement.",
        "medication": {
            "information": "medication may include anticoagulants, antiplatelet medications, beta blockers, diuretics, and blood pressure medications depending on the valve treatment."
        },
        "surgery_info": {
            "purpose": "treats mitral valve stenosis, regurgitation, and other abnormalities that interfere with normal blood flow.",
            "procedure": "the surgeon accesses the heart and repairs the mitral valve by reshaping tissue or inserting a supporting ring. if repair is not possible, the damaged valve is removed and replaced with a biological or mechanical valve."
        },
        "recovery": {
            "overview": "recovery includes postoperative heart monitoring, pain management, incision care, and gradual physical activity. recovery depends on the surgical approach and whether the valve was repaired or replaced.",
            "follow_up": "follow-up includes echocardiograms, cardiology appointments, and monitoring for valve dysfunction or abnormal heart rhythms."
        },
        "risks": ["bleeding", "infection", "stroke", "blood clots", "irregular heartbeat", "valve leakage", "valve failure"]
    },

    "neonatal-and-pediatric-heart-surgery": {
        "name": "neonatal and pediatric heart surgery",
        "category": "congenital heart surgery",
        "description": "an educational overview of neonatal and pediatric heart surgery.",
        "medication": {
            "information": "medication may include diuretics, pain relievers, anticoagulants, antibiotics, and medications that support heart function depending on the child's condition."
        },
        "surgery_info": {
            "purpose": "corrects congenital heart defects such as septal defects, abnormal blood vessels, valve abnormalities, and complex structural conditions.",
            "procedure": "the surgeon accesses the heart and repairs the structural defect. treatment may involve closing abnormal openings, reconstructing blood vessels, repairing valves, or rerouting blood flow."
        },
        "recovery": {
            "overview": "newborns and children may require specialized pediatric cardiac intensive care. monitoring includes oxygen levels, circulation, feeding, heart rhythm, and growth.",
            "follow_up": "follow-up includes pediatric cardiology appointments, echocardiograms, developmental monitoring, and medication adjustments."
        },
        "risks": ["bleeding", "infection", "abnormal heart rhythms", "residual heart defects", "stroke", "organ complications"]
    },

    "nonpharmacological-arrhythmia-therapy": {
        "name": "nonpharmacological arrhythmia therapy",
        "category": "cardiac electrophysiology",
        "description": "an educational overview of nonpharmacological arrhythmia therapy.",
        "medication": {
            "information": "medication may include anticoagulants, beta blockers, and antiarrhythmic medications when needed alongside non-drug treatments."
        },
        "surgery_info": {
            "purpose": "treats abnormal heart rhythms using procedures, electrical devices, or other non-drug interventions.",
            "procedure": "treatment depends on the arrhythmia and may include electrical cardioversion, catheter ablation, pacemaker implantation, or implantable cardioverter-defibrillator placement."
        },
        "recovery": {
            "overview": "recovery varies by treatment. patients may require monitoring after electrical cardioversion or catheter procedures and wound care after device implantation.",
            "follow_up": "follow-up includes ecgs, device checks when applicable, heart rhythm monitoring, and assessment of arrhythmia recurrence."
        },
        "risks": ["abnormal heart rhythms", "blood clots", "stroke", "bleeding", "device complications", "skin irritation after cardioversion"]
    },

    "nuss-procedure": {
        "name": "nuss procedure",
        "category": "thoracic surgery",
        "description": "an educational overview of the nuss procedure.",
        "medication": {
            "information": "medication may include pain relievers, anti-inflammatory medications, and antibiotics depending on the patient's recovery and treatment plan."
        },
        "surgery_info": {
            "purpose": "corrects pectus excavatum, a condition in which the breastbone grows inward, and may improve breathing, exercise tolerance, or chest appearance.",
            "procedure": "the surgeon makes small incisions on both sides of the chest and inserts a curved metal bar behind the breastbone. the bar pushes the breastbone outward and is secured in position."
        },
        "recovery": {
            "overview": "patients may remain hospitalized for pain management and monitoring. physical activity is gradually increased, while heavy lifting and certain twisting movements are restricted during healing.",
            "follow_up": "patients attend surgical appointments and imaging examinations. the metal bar is generally removed in a later procedure after approximately two to three years, depending on age and clinical circumstances."
        },
        "risks": ["bar displacement", "bleeding", "infection", "pneumothorax", "chronic pain", "cardiac injury"]
    },

    "pacemaker-implantation": {
        "name": "pacemaker",
        "category": "cardiac device implantation",
        "description": "an educational overview of pacemaker implantation.",
        "medication": {
            "information": "medication may include antibiotics around implantation, pain relievers, and heart rate medications adjusted according to the patient's condition."
        },
        "surgery_info": {
            "purpose": "treats bradycardia and certain electrical conduction disorders that cause the heart to beat too slowly or irregularly.",
            "procedure": "the surgeon makes an incision below the collarbone and guides electrical leads through a vein into the heart. the leads connect to a pulse generator placed beneath the skin that delivers electrical impulses when needed."
        },
        "recovery": {
            "overview": "patients may go home the same day or after an overnight stay. recovery includes incision care, device testing, and temporary restrictions on heavy lifting and excessive arm movement.",
            "follow_up": "follow-up includes regular device checks, remote monitoring, battery assessments, and cardiology appointments."
        },
        "risks": ["infection", "bleeding", "lead displacement", "pneumothorax", "blood vessel damage", "device malfunction"]
    },

    "percutaneous-valve-procedures": {
        "name": "percutaneous valve procedures",
        "category": "catheter-based valve treatment",
        "description": "an educational overview of percutaneous valve procedures.",
        "medication": {
            "information": "medication may include antiplatelet medications, anticoagulants, and antibiotics depending on the valve procedure and patient's treatment plan."
        },
        "surgery_info": {
            "purpose": "treats selected heart valve conditions while avoiding or reducing the need for open-heart surgery.",
            "procedure": "the surgeon guides a catheter through a blood vessel toward the affected heart valve using medical imaging. specialized devices may repair the valve, reduce leakage, widen a narrowed valve, or replace it."
        },
        "recovery": {
            "overview": "patients are monitored for heart rhythm changes, bleeding, and device function. hospital stays and activity restrictions vary depending on the valve procedure.",
            "follow_up": "follow-up includes echocardiograms, cardiology appointments, and monitoring for valve leakage, narrowing, or device complications."
        },
        "risks": ["bleeding", "stroke", "blood vessel damage", "blood clots", "valve leakage", "device complications", "heart rhythm disturbances"]
    },

    "pulmonary-thromboendarterectomy": {
        "name": "pulmonary thromboendarterectomy",
        "category": "pulmonary vascular surgery",
        "description": "an educational overview of pulmonary thromboendarterectomy.",
        "medication": {
            "information": "medication may include anticoagulants, diuretics, pain relievers, and oxygen therapy depending on the patient's condition and recovery."
        },
        "surgery_info": {
            "purpose": "treats chronic thromboembolic pulmonary hypertension (cteph), a condition in which persistent clots obstruct blood flow through the pulmonary arteries.",
            "procedure": "the surgeon accesses the pulmonary arteries and removes organized blood clots and scar tissue that obstruct blood flow. heart-lung bypass and controlled cooling are commonly required."
        },
        "recovery": {
            "overview": "patients require specialized intensive care monitoring. recovery includes respiratory support, blood pressure monitoring, management of pulmonary pressures, and gradual rehabilitation.",
            "follow_up": "follow-up includes echocardiograms, pulmonary pressure assessments, imaging, exercise evaluation, and long-term anticoagulation when prescribed."
        },
        "risks": ["bleeding", "reperfusion lung injury", "residual pulmonary hypertension", "stroke", "kidney injury", "infection", "heart rhythm disturbances"]
    },
    "pulmonary-valve-repair-and-replacement": {
        "name": "pulmonary valve repair and replacement",
        "category": "heart valve surgery",
        "description": "an educational overview of pulmonary valve repair and replacement.",
        "medication": {
            "information": "medication may include anticoagulants, antiplatelet medications, diuretics, and pain relievers depending on the procedure and patient's condition."
        },
        "surgery_info": {
            "purpose": "treats pulmonary valve stenosis, regurgitation, and other abnormalities that interfere with blood flow from the heart to the lungs.",
            "procedure": "the surgeon repairs the pulmonary valve by reshaping or supporting the existing valve. if repair is not possible, the damaged valve is replaced with a biological or mechanical valve."
        },
        "recovery": {
            "overview": "recovery includes heart rhythm monitoring, pain management, incision care, and gradually returning to normal activities.",
            "follow_up": "follow-up includes cardiology appointments, echocardiograms, and monitoring for valve dysfunction."
        },
        "risks": ["bleeding", "infection", "irregular heartbeat", "blood clots", "valve leakage", "valve failure"]
    },

    "robotic-heart-surgery": {
        "name": "robotic heart surgery",
        "category": "minimally invasive cardiac surgery",
        "description": "an educational overview of robotic heart surgery.",
        "medication": {
            "information": "medication may include pain relievers, antibiotics, anticoagulants, and heart medications depending on the procedure and patient's condition."
        },
        "surgery_info": {
            "purpose": "treats selected cardiovascular conditions using robotic-assisted surgical techniques that may reduce incision size and tissue disruption.",
            "procedure": "the surgeon makes small incisions in the chest and inserts robotic instruments and a camera. the surgeon controls the instruments from a console to perform the required repair or operation."
        },
        "recovery": {
            "overview": "recovery may involve less discomfort and a shorter hospital stay than traditional open surgery, depending on the operation. patients still require monitoring and gradual physical rehabilitation.",
            "follow_up": "follow-up includes surgical evaluations, cardiology appointments, imaging, and incision assessments."
        },
        "risks": ["bleeding", "infection", "blood vessel injury", "irregular heartbeat", "conversion to open surgery", "organ complications"]
    },

    "ross-procedure": {
        "name": "ross procedure",
        "category": "heart valve surgery",
        "description": "an educational overview of the ross procedure.",
        "medication": {
            "information": "medication may include pain relievers, blood pressure medications, and anticoagulants or antiplatelet medications depending on the patient's condition."
        },
        "surgery_info": {
            "purpose": "treats certain aortic valve conditions by replacing the damaged aortic valve with the patient's own pulmonary valve.",
            "procedure": "the surgeon removes the patient's pulmonary valve and places it in the aortic position. a donor pulmonary valve is then used to replace the removed pulmonary valve."
        },
        "recovery": {
            "overview": "recovery includes hospital monitoring, pain management, incision care, and gradual physical activity. patients require monitoring of both the aortic and pulmonary valve positions.",
            "follow_up": "follow-up includes regular echocardiograms and cardiology appointments to monitor both valves and overall heart function."
        },
        "risks": ["bleeding", "infection", "stroke", "irregular heartbeat", "pulmonary valve dysfunction", "aortic valve dysfunction"]
    },

    "transcatheter-aortic-valve-replacement": {
        "name": "transcatheter aortic valve replacement (tavr)",
        "category": "catheter-based heart valve procedure",
        "description": "an educational overview of transcatheter aortic valve replacement.",
        "medication": {
            "information": "medication may include antiplatelet medications, anticoagulants, blood pressure medications, and pain relievers depending on the patient's treatment plan."
        },
        "surgery_info": {
            "purpose": "treats severe aortic valve stenosis by replacing the narrowed valve without requiring traditional open-heart surgery.",
            "procedure": "the surgeon guides a catheter, usually through an artery in the groin, toward the heart. a replacement valve is positioned inside the damaged aortic valve and expanded to restore blood flow."
        },
        "recovery": {
            "overview": "recovery often involves a shorter hospital stay than traditional open-heart valve replacement. patients are monitored for bleeding, heart rhythm changes, and valve function.",
            "follow_up": "follow-up includes echocardiograms, cardiology appointments, and monitoring of the replacement valve and heart function."
        },
        "risks": ["bleeding", "stroke", "blood vessel damage", "heart block", "need for a pacemaker", "valve leakage", "kidney injury"]
    },

    "tricuspid-valve-repair-and-replacement": {
        "name": "tricuspid valve repair and replacement",
        "category": "heart valve surgery",
        "description": "an educational overview of tricuspid valve repair and replacement.",
        "medication": {
            "information": "medication may include diuretics, anticoagulants, pain relievers, and medications that support heart function depending on the patient's condition."
        },
        "surgery_info": {
            "purpose": "treats tricuspid valve regurgitation, stenosis, and other abnormalities that affect blood flow through the right side of the heart.",
            "procedure": "the surgeon repairs the tricuspid valve by reshaping tissue or placing a supporting ring. if repair is not possible, the damaged valve is replaced with a biological or mechanical valve."
        },
        "recovery": {
            "overview": "recovery includes heart monitoring, pain management, incision care, and gradual physical rehabilitation.",
            "follow_up": "follow-up includes echocardiograms, cardiology appointments, and monitoring for fluid buildup, valve dysfunction, and abnormal heart rhythms."
        },
        "risks": ["bleeding", "infection", "stroke", "irregular heartbeat", "blood clots", "valve leakage", "valve failure"]
    },

    "ventricular-assist-device": {
        "name": "ventricular assist device (vad)",
        "category": "mechanical circulatory support",
        "description": "an educational overview of ventricular assist device implantation.",
        "medication": {
            "information": "medication may include anticoagulants, antiplatelet medications, blood pressure medications, and antibiotics to reduce complications and support device function."
        },
        "surgery_info": {
            "purpose": "supports heart function in patients with severe heart failure by helping pump blood from one or both ventricles to the rest of the body.",
            "procedure": "the surgeon implants a mechanical pump that assists the heart in circulating blood. the device is connected to a power source and controller, which may remain outside the body."
        },
        "recovery": {
            "overview": "recovery includes intensive monitoring, device training, incision care, and rehabilitation. patients and caregivers learn how to operate and maintain the device safely.",
            "follow_up": "follow-up includes regular device checks, blood tests, heart failure evaluations, and monitoring for infection, bleeding, and device complications."
        },
        "risks": ["bleeding", "infection", "blood clots", "stroke", "device malfunction", "right heart failure", "kidney complications"]
    },

    "video-assisted-thoracoscopic-surgery": {
        "name": "video-assisted thoracoscopic surgery (vats)",
        "category": "minimally invasive thoracic surgery",
        "description": "an educational overview of video-assisted thoracoscopic surgery.",
        "medication": {
            "information": "medication may include anesthetics, pain relievers, antibiotics, and anticoagulants depending on the procedure and patient's condition."
        },
        "surgery_info": {
            "purpose": "allows surgeons to diagnose and treat conditions inside the chest using smaller incisions instead of a traditional open-chest approach.",
            "procedure": "the surgeon makes small incisions in the chest and inserts a camera and specialized instruments. the camera provides images that guide the surgeon while performing the required procedure."
        },
        "recovery": {
            "overview": "recovery includes breathing exercises, pain management, chest tube monitoring when needed, and gradually increasing physical activity.",
            "follow_up": "follow-up includes surgical appointments, imaging when needed, wound assessments, and monitoring of lung function."
        },
        "risks": ["bleeding", "infection", "pneumonia", "air leakage", "lung injury", "blood clots", "conversion to open surgery"]
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

