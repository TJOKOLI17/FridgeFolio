import { ItemModel } from "./models/ItemModel.js";
import { getItems, updateItem, deleteItem } from "./services/itemService.js";

const populateInventoryList = async () => {
    try {
        const fridgeItems = await getItems() // ItemModel[]
        fridgeItems.forEach((fridgeItem) => {
            toListItem(fridgeItem);
            // setEventListener();
        })
    } catch (error) {
        console.error(error);


    }
}

// const enableEditMode = (event) => {
//     console.log(event)
// }

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
                        <div class="item-amount"><strong> Amount: </strong> <span class="amt-num" onclick="enableEditMode(event, ${item.id}, '${item.name}', ${item.amount}, '${item.expDate})">${item.amount}</span></div> 
                        <div class="item-exp-date last-day"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> <span class="amt-num" onclick="enableEditMode(event, ${item.id}, '${item.name}', ${item.amount}, '${item.expDate}')</span></div> 
                        <div class="item-exp-date"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    }

    listItem.classList.add('list-item');

    const deleteBtn = document.createElement('img');
    deleteBtn.src = '../img/delete-icon.png';
    deleteBtn.alt = 'Delete';
    deleteBtn.classList.add('delete-btn');

    // Attach the event listener for deleting the item
    deleteBtn.addEventListener('click', () => deleteItem(item));

    // Append the button and list item
    listItem.appendChild(deleteBtn);
    inventoryList.appendChild(listItem);
    inventoryList.appendChild(document.createElement('br'));
};

const isExpired = (date, check = null) => {
    const today = new Date(String(new Date().toLocaleDateString()))

    if (check == "today") {
        const todayAsString = `${new Date().getFullYear()}/${new Date().getMonth() + 1}/${new Date().getDate()}`
        return date === todayAsString
    }

    return new Date(date) < today
}


window.enableEditMode = enableEditMode;
// function enableEditMode(event) {
//     let numSpan = event.target
//     const origValue = Number(numSpan.textContent);
//     const input = document.createElement('input');
//     input.type = 'number';
//     input.value = origValue;
//     input.className = 'editable-num';

//     numSpan.replaceWith(input)
//     input.focus();

//     input.addEventListener("keydown", async (event) => {
//         if (event.key == "Enter") {
//             // console.log(typeof input.value)
//             const newValue = Number(input.value)
//             if (!isNaN(Number(input.value) && newValue > 0)) {
//                 // console.log(typeof newValue)
//                 // console.log(Number("2-"));
//                 console.log("1st If Statment this is a number", !isNaN(input.value));
//                 if (origValue != newValue) {
//                     await refreshItem(newValue)
//                 }
//                 const updatedSpan = document.createElement('span');
//                 updatedSpan.className = 'amt-num';
//                 updatedSpan.textContent = newValue || origValue;

//                 // Replace the input with the new span and re-add the event listener
//                 input.replaceWith(updatedSpan);
//                 updatedSpan.addEventListener('click', enableEditMode);
//             } else { // input value is not a number, so revert back to original value
//                 console.log("2nd If Statment this is a number", !isNaN(input.value));

//                 const updatedSpan = document.createElement('span');
//                 updatedSpan.className = 'amt-num';
//                 updatedSpan.textContent = origValue;

//                 // Replace the input with the new span and re-add the event listener
//                 input.replaceWith(updatedSpan);
//                 updatedSpan.addEventListener('click', enableEditMode);
//             }
//         }
//     })
// }

function enableEditMode(event, ...item) {
    let numSpan = event.target;
    const origValue = Number(numSpan.textContent); // Get the original value as a number
    const input = document.createElement('input');
    input.type = 'number';
    input.value = origValue;
    input.className = 'editable-num';

    numSpan.replaceWith(input);  // Replace the span with the input
    input.focus();  // Focus on the input for editing

    input.addEventListener("keydown", async (event) => {
        if (event.key === "Enter") {
            const newValue = Number(input.value);  // Convert the input value to a number
            // Check if the new value is a valid number and greater than or equal to 0
            if (!isNaN(newValue) && newValue >= 0) {
                // Only refresh the item if the new value is different from the original value
                if (origValue !== newValue) {
                    await refreshItem(newValue, item);  // Call your refresh function with the new value
                }
                backToSpan(input, newValue);
            } else {
                backToSpan(input, origValue);
            }
        }
    });
}

const backToSpan = (input, value) => {
    const updatedSpan = document.createElement('span');
    updatedSpan.className = 'amt-num';
    updatedSpan.textContent = value;

    // Replace the input with the original value and re-add the event listener
    input.replaceWith(updatedSpan);
    updatedSpan.addEventListener('click', enableEditMode);
}


const refreshItem = async (newValue, item) => {
    const modifiedItem = new ItemModel(item[0], item[1], newValue, item[3])
    console.log(modifiedItem)
    return updateItem(modifiedItem)


}


populateInventoryList()