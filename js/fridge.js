import { getItems, deleteItem } from "./services/itemService.js";

const populateInventoryList = async () => {
    try {
        const fridgeItems = await getItems() // ItemModel[]
        fridgeItems.forEach((fridgeItem) => { toListItem(fridgeItem) })
    } catch (error) {
        console.error(error);


    }
}


const toListItem = (item) => {
    const inventoryList = document.getElementById('inventory-list');
    // Create the list item
    const listItem = document.createElement('li');

    if (isExpired(item.expDate)) {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> ${item.amount}</div> 
                        <div class="item-exp-date expired"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> ${item.amount}</div> 
                        <div class="item-exp-date"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    }

    listItem.classList.add('list-item');

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
};

const isExpired = (date) => {
    const today = new Date(String(new Date().toLocaleDateString()))
    return new Date(date) < today
}

populateInventoryList()