function addToInventory() {
    const nameInput = document.getElementById("name").value;
    const amountInput = document.getElementById("amount").value;
    const expYearInput = document.getElementById("expiration-year").value;
    const expMonthInput = document.getElementById("expiration-month").value;
    const expDayInput = document.getElementById("expiration-day").value;

    

    if(!nameInput || !amountInput || !expYearInput || !expMonthInput || !expDayInput){
        window.alert("Please provide information for all the fields.")
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
        `Name: ${nameInput}<br> 
        Amount: ${amountInput}<br>  
        Expiration Year: ${expYearInput}<br>  
        Expiration Month: ${expMonthInput}<br>  
        Expiration Day: ${expDayInput}<br><br> `
        inventoryList.appendChild(listItem);
    }
  }