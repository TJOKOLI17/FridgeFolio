import { ItemModel } from "./models/ItemModel.js";
import { getUserItems, updateItem } from "./services/itemService.js";
import { toListItem, redirectToHome, restrictPageContent } from "./services/sharedService.js";
let boundHandler;

const populateInventoryList = async () => {
    const itemListTitle = document.getElementById('item-list-title');
    itemListTitle.textContent = `What's In Your Fridge, ${localStorage.getItem("username")}`

    const inventoryList = document.getElementById('inventory-list');
    inventoryList.replaceChildren();
    try {
        const fridgeItems = await getUserItems() // ItemModel[]
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

const updateInventoryList = (item_id) => {
    const inventoryList = document.getElementById('inventory-list');
    const listItems = document.querySelectorAll("li")

    listItems = Array.of(listItems).filter((listItem) => { listItem })
}


const backToSpan = (amountInput, value, item) => {
    amountInput.removeEventListener("keydown", boundHandler);
    const updatedSpan = document.createElement('span');
    updatedSpan.className = 'amt-num';
    updatedSpan.textContent = value;

    // Replace the input with the original value and re-add the event listener
    updatedSpan.addEventListener('click', (event) => enableEditMode(event, item));
    amountInput.replaceWith(updatedSpan);

}


const updateListItem = async (newValue, item) => {

    const [ID, UID, NAME, EXPDATE] = [0, 1, 2, 4];
    const modifiedItem = new ItemModel(item[ID], item[UID], item[NAME], newValue, item[EXPDATE])
    await updateItem(modifiedItem)
}

const filterItems = () => {
    const query = document.getElementById('search-bar').value.toLowerCase();
    const listItems = document.querySelectorAll('#inventory-list > li, #inventory-list > br');

    listItems.forEach((item) => {
        if (item.tagName === 'LI') {
            const itemName = item.querySelector('.item-name').textContent.toLowerCase();
            item.style.display = itemName.includes(query) ? '' : 'none';
        } else if (item.tagName === 'BR') {
            // Handle <br>: Show only if the previous <li> is visible
            const prevElement = item.previousElementSibling;
            item.style.display = prevElement && prevElement.style.display !== 'none' ? '' : 'none';
        }
    });
};

document.getElementById('search-bar').addEventListener('input', filterItems);

restrictPageContent()
redirectToHome()
populateInventoryList()

