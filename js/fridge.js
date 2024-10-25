import { getItems, deleteItem } from "./services/itemService.js";

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
    const listItem = document.createElement('li');
    listItem.innerHTML = `<strong>Name:</strong> ${item.name} | 
                    <strong> Amount: </strong> ${item.amount} | 
                    <strong> Expiration Date: </strong> ${item.expDate}`;

    listItem.classList.add('list-item');

    // Create the delete button
    // const deleteBtn = document.createElement('button');
    // deleteBtn.textContent = 'Delete';
    // deleteBtn.classList.add("delete-btn")

    const deleteBtn = document.createElement('img');
    deleteBtn.src = '../img/delete-icon.png'; // Replace with the correct path
    deleteBtn.alt = 'Delete';
    deleteBtn.classList.add('delete-btn');

    // Attach the event listener for deleting the item
    deleteBtn.addEventListener('click', () => deleteItem(item));

    // Append the button and list item
    listItem.appendChild(deleteBtn);
    inventoryList.appendChild(listItem);
    inventoryList.appendChild(document.createElement('br'));
    inventoryList.classList.add("item-container")
};

populateInventoryList()