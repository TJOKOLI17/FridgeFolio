/**
 * FridgeFolio
 * @author Tobenna Okoli, Luis Fajardo
 * @copyright 2024
 */

import { getItems, deleteItem } from "./itemService.js";

/**
 * Check if item is expired or expires today.
 * @param date item's expiration date.
 * @param check optional paramter to check if item expires today.
 */
export const isExpired = (date, check = null) => {
    const today = new Date(String(new Date().toLocaleDateString()))

    if (check == "today") {
        const todayAsString = `${new Date().getFullYear()}/${new Date().getMonth() + 1}/${new Date().getDate()}`
        return date === todayAsString
    }

    return new Date(date) < today
}

/**
 * Create list item element for UI representation of fridge item.
 * @param list HTML list element to append fridge item to.
 * @param item object containing fridge item data.
 * @param inTrash checks if item is in trash or not.
 */
export const toListItem = (list, item, inTrash) => {
    const listItem = document.createElement('li');

    if (isExpired(item.expDate)) {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> <span class="${!inTrash ? `amt-num` : ''}" onclick="${!inTrash ? `enableEditMode(event, ${item.id}, '${item.name}', ${item.amount}, '${item.expDate}')` : ''}">${item.amount}</span></div> 
                        <div class="item-exp-date expired"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else if (isExpired(item.expDate, "today")) {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> <span class="${!inTrash ? `amt-num` : ''}" onclick="${!inTrash ? `enableEditMode(event, ${item.id}, '${item.name}', ${item.amount}, '${item.expDate}')` : ''}">${item.amount}</span></div> 
                        <div class="item-exp-date last-day"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> <span class="${!inTrash ? `amt-num` : ''}" onclick="${!inTrash ? `enableEditMode(event, ${item.id}, '${item.name}', ${item.amount}, '${item.expDate}')` : ''}">${item.amount}</span></div> 
                        <div class="item-exp-date"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    }

    listItem.classList.add('list-item');

    if (!inTrash) {
        list.appendChild(listItem);
        list.appendChild(document.createElement('br'));

        const deleteBtn = document.createElement('img');
        deleteBtn.src = '../img/delete-icon.png';
        deleteBtn.alt = 'Delete';
        deleteBtn.classList.add('delete-btn');

        // Attach the event listener for deleting the item
        deleteBtn.addEventListener('click', () => deleteItemAndRefreshInventoryList(item));

        // Append the button and list item
        listItem.appendChild(deleteBtn);
    }

    return listItem;
}

const deleteItemAndRefreshInventoryList = async (deletedItem) => {
    // console.log(isExpired(deletedItem.expDate));
    // if (deletedItem.amount > 0 || !isExpired(deletedItem.expDate)) {
    //     window.alert("Item must be expired or have 0 quantity to be deleted.")
    // } else {
    //     await deleteItem(deletedItem)
    // }

    if (deletedItem.amount === 0 || isExpired(deletedItem.expDate)) {
        await deleteItem(deletedItem)
        try {
            const inventoryList = document.getElementById('inventory-list');
            inventoryList.replaceChildren();
            const fridgeItems = await getItems() // ItemModel[]
            fridgeItems.forEach((fridgeItem) => {
                toListItem(inventoryList, fridgeItem, false);
            })
        } catch (error) {
            console.error(error);


        }

        return;
    }

    window.alert("Item must be expired or have 0 quantity to be deleted.")
}

/**
 * Prevent user from going back to website if they logged out.
 */
export const redirectToHome = () => {
    if (!isLoggedIn()) {
        window.location.href = "index.html"
    }
}

/**
 * Checks if user is logged in or not.
 * @returns 
 */
const isLoggedIn = () => {
    if (localStorage.getItem("username") != null && localStorage.getItem("uid") != null) {
        return true
    }

    return false
}

// document.addEventListener("click", (event) => {
//     const newValue = Number(String(amountInput.value));  // Convert the input value to a number
//     if (!amountInput.contains(event.target) && !(event.target instanceof HTMLSpanElement)) {  // Check if click was outside the amountInput
//         // console.log("You clicked outside the input");
//         console.log(amountInput instanceof HTMLInputElement)
//         // console.log(event.target);

//         // backToSpan(amountInput, newValue, item);
//         handleAmountInputUpdate(event, origValue, newValue, amountInput, item);
//     } else {
//         console.log("You did NOT click outside the input");
//     }
// });