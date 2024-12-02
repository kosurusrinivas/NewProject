let designations = ["Chief Executive Officer",
    "Center Manager",
    "SAP Abap Consultant",
    "Maintenance Manager",
    "Maintenance Supervisor",
    "Emergency Medical Technician",
    "Employee Relations Executive",
    "Embedded Engineer",
    "Emergency Medical Technician",
    "Embedded Software Engineer",
];

let sorteddesignation = designations.sort();

let input = document.getElementById("input");

input.addEventListener("keyup", (e) => {
    removeElements();
    for(let i of sorteddesignation){
        
        if (i.toLowerCase().startsWith(input.value.toLowerCase()) && input.value != ""){
            let listItem = document.createElement("li");
            listItem.classList.add("list-items");
            listItem.style.cursor = "pointer";
            listItem.setAttribute("onclick", "displayName('"+ i +"')");
            let word =  i.substr(0,input.value.length);
            word += i.substr(input.value.length);
            listItem.innerHTML = word;
            document.querySelector(".list").appendChild(listItem);
        }
    }
});

function displayName(value){
    input.value = value;
    removeElements()

}

function removeElements(){
    let items = document.querySelectorAll(".list-items");
    items.forEach((item)=>{
        item.remove();
    });
}