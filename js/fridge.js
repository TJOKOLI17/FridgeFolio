import { ItemModel } from "./models/ItemModel.js";
import { getItems, updateItem } from "./services/itemService.js";
import { toListItem } from "./services/sharedService.js";
let boundHandler;

const populateInventoryList = async () => {
    const inventoryList = document.getElementById('inventory-list');
    inventoryList.replaceChildren();
    try {
        const fridgeItems = await getItems() // ItemModel[]
        fridgeItems.forEach((fridgeItem) => {
            inventoryList.append(toListItem(inventoryList, fridgeItem, false));
            inventoryList.appendChild(document.createElement('br'));
        })
    } catch (error) {
        console.error(error);


    }
}


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

    boundHandler = async (event) => {
        const newValue = Number(String(amountInput.value));  // Convert the input value to a number
        await handleAmountInputUpdate(event, origValue, newValue, amountInput, item)
    };

    // Attach the keydown event listener with the actual event passed to the handler
    amountInput.addEventListener("keydown", boundHandler);
}


const handleAmountInputUpdate = async (event, origValue, newValue, amountInput, item) => {
    if (event.key === "Enter") {

        if (!isNaN(newValue) && newValue >= 0 && amountInput.value !== "") {
            // Only refresh the item if the new value is different from the original value
            if (origValue !== newValue) {
                await updateListItem(newValue, item);  // Call your refresh function with the new value
            } else {
            }
            backToSpan(amountInput, newValue, item);
            populateInventoryList()
        } else {

            backToSpan(amountInput, origValue, item);
            populateInventoryList()
        }
    }
}


const backToSpan = (amountInput, value, item) => {
    amountInput.removeEventListener("keydown", boundHandler);
    const updatedSpan = document.createElement('span');
    updatedSpan.className = 'amt-num';
    updatedSpan.textContent = value;

    // Replace the input with the original value and re-add the event listener
    updatedSpan.addEventListener('click', enableEditMode);
    amountInput.replaceWith(updatedSpan);

}


const updateListItem = async (newValue, item) => {
    const modifiedItem = new ItemModel(item[0], item[1], newValue, item[3])
    await updateItem(modifiedItem)
}

populateInventoryList()