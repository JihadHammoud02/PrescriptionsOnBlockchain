// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

contract Doctors{
    uint numberAdmins=10;
    // Creating a dynamic array of Admins
    address[] Admins = new address[](numberAdmins);

    // Adding an admin to the array of Admins
    function addAdmin(address adminAddress) public  {
        Admins.push(adminAddress);
    }

    // Verifying if input address is Admin
    function containAdmin(address add) public view returns(bool) {
        bool isAdmin = false;
        uint i=0;
        while(!isAdmin && i<Admins.length){
            isAdmin = add == Admins[i];
            i=i+1;
        }
        return isAdmin;
    }

    // function only for Admins (testing...)
    function onlyAdmin(address add) public view returns(bool) {
        return containAdmin(add);
    }
}