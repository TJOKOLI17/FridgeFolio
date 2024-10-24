import { getItems, deleteItem } from "./itemService.js";

const populateInventoryList = async () => {
    try {
        const fridgeItems = await getItems() // ItemModel[]
        for (let fridgeItem of fridgeItems) {
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