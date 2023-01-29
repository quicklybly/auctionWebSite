const myBirthDateString = "2003-10-10"

function printMyAge() {
    printAge(myBirthDateString)
}

function printAge(birthDateString) {
    document.write(getAge(birthDateString))
}

function getAge(birthDateString) {
    let today = new Date();
    let birthDate = new Date(birthDateString);
    let age = today.getFullYear() - birthDate.getFullYear();
    let months = today.getMonth() - birthDate.getMonth();
    if (months < 0 || (months === 0 && today.getDate() < birthDate.getDate())) {
        --age;
    }
    return age;
}