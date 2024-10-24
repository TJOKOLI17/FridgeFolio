// import { ItemModel } from "./model";

class ItemModel {
    constructor(id, name, amount, expDate) {
        this.id = id
        this.name = name;
        this.amount = amount;
        this.expDate = expDate;
    }
}

const apiKey = "http://127.0.0.1:8000"

const itemSubmit = document.getElementById("item-submit")

itemSubmit.addEventListener('submit', async (event) => {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const amount = document.getElementById("amount").value;
    const expYear = Number(document.getElementById("expYear").value);
    const expMonth = Number(document.getElementById("expMonth").value);
    const expDay = Number(document.getElementById("expDay").value);
    const expDate = `${expYear}/${expMonth}/${expDay}`

    if (!name || !amount || !expYear || !expMonth || !expDay) {
        window.alert("Please provide information for all the fields.")
    } else if (typeof (expDay) !== "number" || typeof (expMonth) !== "number" || typeof (expYear) !== "number") {
        window.alert("Please enter valid numbers for date information")
    } else {
        try {
            newItem = await addItem({
                name: name,
                amount: amount,
                expDate: expDate
            })

            console.log(newItem.name, newItem.amount, newItem.expDate);
            itemSubmit.reset()
        } catch (error) {
            window.alert(error)
        }

    }
})


/*async function addItemToInventory() {
    // console.log(event)
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
            newItem = await addItem({
                name: name,
                amount: amount,
                expDate: expDate
            })

            console.log(newItem.name, newItem.amount, newItem.expDate);

        } catch (error) {
            window.alert(error)
        }

    }
}*/

const getItems = async () => {
    try {
        let fridge = [];
        response = await fetch(apiKey);
        if (!response.ok) {
            throw new Error("Error in fetching fridge items")
        }
        const allItems = await response.json()
        for (item of allItems) {
            fridge.push(new ItemModel(item.id, item.name, item.amount, item.expDate))
        }
        return fridge
    } catch (error) {
        console.error(error);

    }
}

const addItem = async (newItem) => {
    try {
        const response = await fetch(apiKey, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newItem),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const currentItem = await response.json();
        console.log('Success:', currentItem);

        return new ItemModel(
            currentItem.id,
            currentItem.name,
            currentItem.amount,
            currentItem.expDate
        )
    } catch (error) {
        throw new Error(error)
    }
}

const updateItem = async (id) => { }

const deleteItem = async (item) => {
    try {
        await fetch(`${apiKey}/${item.id}`, {
            method: 'DELETE',
        });
    } catch (error) {
        throw new Error(error)
    }
    // console.log(item);
}

const populateInventoryList = async () => {
    try {
        fridgeItems = await getItems() // ItemModel[]
        for (fridgeItem of fridgeItems) {
            toListItem(fridgeItem)
        }
    } catch (error) {
        console.error(error);


    }
}

const toListItem = (item) => {
    const inventoryList = document.getElementById('inventory-list');

    // Create the list item
    const li = document.createElement('li');
    li.innerHTML = `Name: ${item.name} | Amount: ${item.amount} | Expiration Date: ${item.expDate}`;

    // Create the delete button
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';

    // Attach the event listener for deleting the item
    deleteButton.addEventListener('click', () => deleteItem(item));

    // Append the button and list item
    li.appendChild(deleteButton);
    inventoryList.appendChild(li);
};


populateInventoryList()



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