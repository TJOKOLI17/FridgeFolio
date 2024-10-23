// import { Item } from "./item";

function addToInventory() {
    const name = document.getElementById("name").value;
    const amount = document.getElementById("amount").value;
    const expYear = Number(document.getElementById("expiration-year").value);
    const expMonth = Number(document.getElementById("expiration-month").value);
    const expDay = Number(document.getElementById("expiration-day").value);
    const expDate = `${expYear}/${expMonth}/${expDay}`
    console.log(typeof expDate)


    if (!name || !amount || !expYear || !expMonth || !expDay) {
        window.alert("Please provide information for all the fields.")
    } else if (typeof (expDay) !== "number" || typeof (expMonth) !== "number" || typeof (expYear) !== "number") {
        window.alert("Please enter valid numbers for date information")
    } else {
        // Clear the input values
        {
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

        // item

    }
}

// Example of using fetch to POST data to a FastAPI endpoint

// const postData = async () => {
//     const data = {
//         name: "John Doe",
//         age: 30
//     };

//     try {
//         const response = await fetch('http://localhost:8000/your-endpoint', {
//             method: 'POST', // or 'PUT'
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify(data),
//         });

//         if (!response.ok) {
//             throw new Error(`HTTP error! status: ${response.status}`);
//         }

//         const responseData = await response.json();
//         console.log('Success:', responseData);
//     } catch (error) {
//         console.error('Error:', error);
//     }
// };

// postData();


const apiKey = "http://127.0.0.1:8000"
const fetchItems = async () => {
    try {
        response = await fetch(apiKey);
        if (!response.ok) {
            throw new Error("Error in fetching fridge items")
        }

        data = await response.json()
        console.log(data[0]);

    } catch (error) {
        console.error(error);

    }
}