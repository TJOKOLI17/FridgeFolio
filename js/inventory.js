function addToInventory() {
    const name = document.getElementById("name").value;
    const amount = document.getElementById("amount").value;
    const expYear = Number(document.getElementById("expiration-year").value);
    const expMonth = Number(document.getElementById("expiration-month").value);
    const expDay = Number(document.getElementById("expiration-day").value);
    const expDate = `${expMonth}/${expDay}/${expYear}`
    console.log(typeof expDate)
    
    
    if (!name || !amount || !expYear || !expMonth || !expDay){
        window.alert("Please provide information for all the fields.")
    }else if (typeof(expDay) !== "number" || typeof(expMonth) !== "number" || typeof(expYear) !== "number"){
        window.alert("Please enter valid numbers for date information")
    }else{
        // Clear the input values
        document.getElementById("name").value = "";
        document.getElementById("amount").value = "";
        document.getElementById("expiration-year").value = "";
        document.getElementById("expiration-month").value = "";
        document.getElementById("expiration-day").value = "";

        // Display the entered data in a list
        const inventoryList = document.getElementById("inventoryList");
        const listItem = document.createElement("li");
        listItem.innerHTML = 
        `Name: ${name}<br> 
        Amount: ${amount}<br> 
        Expiration Date: ${expDate}`
        inventoryList.appendChild(listItem);
    }
}