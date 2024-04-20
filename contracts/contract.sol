// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract DoctorApp {
    struct Prescription {
        address patientAddress;
        string normalMedication;
        string normalDosage;
        string brandedMedication;
        string brandedDosage;
        string age;
        string diagnoses;
        uint timestamp;
    }

    struct Doctor {
        string name;
        string specialty;
    }

    address[] private Admins;
    address[] private Doctors;
    address[] private patients;
    
    mapping(address => Prescription[]) private prescriptions;
    mapping(address => Doctor) private doctorInfo;

    modifier onlyAdmin() {
        require(isAdmin(msg.sender), "Not an admin");
        _;
    }

    modifier onlyDoctor() {
        require(isDoctor(msg.sender), "Not a doctor");
        _;
    }

    constructor() {
        
        Admins.push( 0x09DE81704a9e21166089e99423721648e6C52f29);
    }

    function isAdmin(address user) public view returns(bool) {
        for (uint i = 0; i < Admins.length; i++) {
            if (Admins[i] == user) return true;
        }
        return false;
    }

    function isDoctor(address user) public view returns(bool) {
        for (uint i = 0; i < Doctors.length; i++) {
            if (Doctors[i] == user) return true;
        }
        return false;
    }

    function addAdmin(address admin) public onlyAdmin {
        Admins.push(admin);
    }

    function addDoctor(address doctor, string memory name, string memory specialty) public onlyAdmin {
        require(!isDoctor(doctor), "Doctor already exists");

        Doctors.push(doctor);
        doctorInfo[doctor] = Doctor(name, specialty);
    }

    function removeAdmin(address admin) public onlyAdmin {
        for (uint i = 0; i < Admins.length; i++) {
            if (Admins[i] == admin) {
                for (uint j = i; j < Admins.length - 1; j++) {
                    Admins[j] = Admins[j + 1];
                }
                Admins.pop();
                break;
            }
        }
    }

    function getDoctors() public view returns (address[] memory) {
        return Doctors;
    }

    function addPrescription(
        address patientAddress, 
        string memory normalMedication, 
        string memory normalDosage, 
        string memory brandedMedication, 
        string memory brandedDosage,
        string memory age,
        string memory diagnoses) public onlyDoctor {
        patients.push(patientAddress);
        require(bytes(normalMedication).length > 0 && bytes(normalDosage).length > 0, "Normal prescription is required");
        
        if (bytes(brandedMedication).length > 0) {
            require(bytes(brandedDosage).length > 0, "Branded dosage is required with branded medication");
        }
        
        prescriptions[patientAddress].push(
            Prescription(
                patientAddress,
                normalMedication,
                normalDosage,
                brandedMedication,
                brandedDosage,
                 age,
                 diagnoses,
                block.timestamp
            )
        );
    }

    function getPrescriptions(address patientAddress) public view returns (Prescription[] memory) {
        return prescriptions[patientAddress];
    }

    function getDoctorInfo(address doctor) public view returns (string memory name, string memory specialty) {
        require(isDoctor(doctor), "Not a doctor");
        Doctor memory doctorDetails = doctorInfo[doctor];
        return (doctorDetails.name, doctorDetails.specialty);
    }

    function getPatients() public view returns (address[] memory){
        return patients;
    }
}
