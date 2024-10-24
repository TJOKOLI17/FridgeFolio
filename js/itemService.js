// import { ItemModel } from "./model";

class ItemModel {
    constructor(id, name, amount, expDate) {
        this.id = null
        this.name = name;
        this.amount = amount;
        this.expDate = expDate;
    }
}

const apiKey = "http://127.0.0.1:8000"

async function addItemToInventory(event) {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const amount = document.getElementById("amount").value;
    const expYear = Number(document.getElementById("expiration-year").value);
    const expMonth = Number(document.getElementById("expiration-month").value);
    const expDay = Number(document.getElementById("expiration-day").value);
    const expDate = `${expYear}/${expMonth}/${expDay}`

    if (!name || !amount || !expYear || !expMonth || !expDay) {
        window.alert("Please provide information for all the fields.")
    } else if (typeof (expDay) !== "number" || typeof (expMonth) !== "number" || typeof (expYear) !== "number") {
        window.alert("Please enter valid numbers for date information")
    } else {
        try {
            await addItem({
                name: name,
                amount: amount,
                expDate: expDate
            })
        } catch (error) {
            window.alert(error)
        }

    }
}


const getItems = async () => {
    try {
        response = await fetch(apiKey);
        if (!response.ok) {
            throw new Error("Error in fetching fridge items")
        }
        data = await response.json()
        console.log(data);

    } catch (error) {
        console.error(error);

    }
}

const addItem = async (newItem) => {
    try {
        const response = await fetch(apiKey, {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newItem),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('Success:', responseData);
    } catch (error) {
        throw new Error(error)
    }
}

const updateItem = async (id) => { }

const deleteItem = async (id) => { }

/* // Clear the input values
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
*/