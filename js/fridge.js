import { ItemModel } from "./models/ItemModel.js";
import { getItems, updateItem, deleteItem } from "./services/itemService.js";
import { isExpired } from "./services/helperService.js";

const populateInventoryList = async () => {
    try {
        const inventoryList = document.getElementById('inventory-list');
        inventoryList.replaceChildren();
        const fridgeItems = await getItems() // ItemModel[]
        fridgeItems.forEach((fridgeItem) => {
            toListItem(fridgeItem);
        })
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
                        <div class="item-amount"><strong> Amount: </strong> <span class="amt-num" onclick="enableEditMode(event, ${item.id}, '${item.name}', ${item.amount}, '${item.expDate}')">${item.amount}</span></div> 
                        <div class="item-exp-date expired"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else if (isExpired(item.expDate, "today")) {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> <span class="amt-num" onclick="enableEditMode(event, ${item.id}, '${item.name}', ${item.amount}, '${item.expDate}')">${item.amount}</span></div> 
                        <div class="item-exp-date last-day"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> <span class="amt-num" onclick="enableEditMode(event, ${item.id}, '${item.name}', ${item.amount}, '${item.expDate}')">${item.amount}</span></div>
                        <div class="item-exp-date"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    }

    listItem.classList.add('list-item');

    const deleteBtn = document.createElement('img');
    deleteBtn.src = '../img/delete-icon.png';
    deleteBtn.alt = 'Delete';
    deleteBtn.classList.add('delete-btn');

    // Attach the event listener for deleting the item
    deleteBtn.addEventListener('click', () => deleteItemAndRefreshInventoryList(item));

    // Append the button and list item
    listItem.appendChild(deleteBtn);
    inventoryList.appendChild(listItem);
    inventoryList.appendChild(document.createElement('br'));
};



window.enableEditMode = enableEditMode;
function enableEditMode(event, ...item) {
    let amountSpan = event.target;
    const origValue = Number(amountSpan.textContent); // Get the original value as a number
    const amountInput = document.createElement('input');
    amountInput.type = 'number';
    amountInput.value = origValue;
    amountInput.className = 'editable-num';

    amountSpan.replaceWith(amountInput);  // Replace the span with the input
    amountInput.focus();  // Focus on the input for editing

    amountInput.addEventListener("keydown", async (event) => {
        if (event.key === "Enter") {
            // event.preventDefault()

            // if (amountInput.value === "") {
            //     console.log("value is empty");

            // }
            // console.log(`amountInput.value: ${amountInput.value}, type of amountInput.value ${typeof amountInput.value}`)
            // console.log(`newValue: ${newValue}, type of newValue ${typeof newValue}`)
            // Check if the new value is a valid number and greater than or equal to 0
            const newValue = Number(String(amountInput.value));  // Convert the input value to a number

            if (!isNaN(newValue) && newValue >= 0 && amountInput.value !== "") {
                // Only refresh the item if the new value is different from the original value
                if (origValue !== newValue) {
                    await updateItemAndRefreshInventoryList(newValue, item);  // Call your refresh function with the new value
                }
                backToSpan(amountInput, newValue, item);
                populateInventoryList()
            } else {
                backToSpan(amountInput, origValue, item);
                populateInventoryList()
            }
        }
    });
}

const backToSpan = (input, value, item) => {
    const updatedSpan = document.createElement('span');
    updatedSpan.className = 'amt-num';
    updatedSpan.textContent = value;

    // Replace the input with the original value and re-add the event listener
    updatedSpan.addEventListener('click', enableEditMode);
    // updatedSpan.addEventListener('click', () => { enableEditMode(event, item) });
    input.replaceWith(updatedSpan);
}


const updateItemAndRefreshInventoryList = async (newValue, item) => {
    const modifiedItem = new ItemModel(item[0], item[1], newValue, item[3])
    await updateItem(modifiedItem)
    populateInventoryList()
}

const deleteItemAndRefreshInventoryList = async (deletedItem) => {
    await deleteItem(deletedItem)
    populateInventoryList()
}

// const checkifNan = () => {
//     let num = Number("2-")
//     console.log(`${num} is not a number: ${isNaN(num)}`)
// }

// checkifNan()
populateInventoryList()