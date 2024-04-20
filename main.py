from fastapi import FastAPI
from pydantic import BaseModel
import AuthSC as sc
from fastapi.middleware.cors import CORSMiddleware

class Wallet(BaseModel):
    pk: str
    privKey: str

class PrescriptionData(BaseModel):
    patientAddress: str
    normalMedication: str
    normalDosage: str
    brandedMedication: str = ""
    brandedDosage: str = ""
    age: str=""
    diagnoses: str=""
    pk: str
    privKey: str

class DoctorInfo(BaseModel):
    address: str
    name: str
    specialty: str
    pk: str
    privKey: str


class AdminInfo(BaseModel):
    address: str
    pk: str
    privKey: str

app = FastAPI()

origins = [
   "http://127.0.0.1:5500"
    # Add more allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.post("/connect")
async def connect(wallet: Wallet):
    if sc.verify_keys(wallet.pk, wallet.privKey) and sc.containAdmin(wallet.pk):
        return {"authentication": "Admin"}
    if sc.verify_keys(wallet.pk, wallet.privKey) and sc.containDoctor(wallet.pk):
        return {"authentication": "Doc"}
    return {"authentication": "Failed"}

@app.post("/addDoctor")
async def addDoctor(doc:DoctorInfo):
    sc.addDoctor(doc.address,doc.name,doc.specialty,doc.pk,doc.privKey)
    return {"add":"Success"}

@app.post("/addAdmin")
async def add_admin(admin: AdminInfo):
    try:
        sc.addAdmin(admin.address, admin.pk, admin.privKey)
        return {"add": "Success"}
    except Exception as e:
        print(e)
        return {"add": "Failed"}
    

@app.post("/addPrescription")
async def add_prescription(prescription: PrescriptionData):
        print("EJU")
        tx_receipt = sc.addPrescription(prescription.patientAddress, prescription.normalMedication, prescription.normalDosage, prescription.brandedMedication, prescription.brandedDosage,prescription.age,prescription.diagnoses,prescription.pk,prescription.privKey)
        print(tx_receipt)
        return {"result": "Prescription added"}
    

@app.get("/getPrescriptions/{patientAddress}")
async def get_prescriptions(patientAddress: str):
    prescriptions = sc.get_prescriptions(patientAddress)
    return {"prescriptions": prescriptions}

@app.get("/getPatients")
async def get_patients():
    patients = sc.get_patients()
    return {"prescriptions": patients}



@app.get("/getDoctors", response_model=list[DoctorInfo])
async def get_doctors():
    doctors_addresses = sc.get_doctors()
    doctors_info = []
    for doctor_address in doctors_addresses:
        name, specialty = sc.get_doctor_info(doctor_address)
        doctors_info.append(DoctorInfo(address=doctor_address, name=name, specialty=specialty))
    return doctors_info
