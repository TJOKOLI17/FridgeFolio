/**
 * FridgeFolio
 * @author Tobenna Okoli, Luis Fajardo
 * @copyright 2024
 */
import { getUserItems, deleteItem } from "./itemService.js";

const HOME_PAGE = "index.html"


/**
 * Check if item is expired or expires today.
 * @param date item's expiration date.
 * @param check optional paramter to check if item expires today.
 * @returns {boolean} if item is expired (true), expires today (true), or is still good (false).
 */
export const isExpired = (date, check = null) => {
    let today = new Date(String(new Date().toLocaleDateString()))

    if (check == "today") {
        today = `${today.getFullYear()}/${String(today.getMonth() + 1).padStart(2, '0')}/${String(today.getDate()).padStart(2, '0')}`;
        return date === today
    }

    return new Date(date) < today
}

/**
 * convert raw createdAt user property to a valid string.
 * @param {string} createdAt 
 * @returns {string} properly formatted createdAt date.
 */
// export const formatCreatedAt = (createdAt) => {
//     const date = new Date(createdAt); // Convert to Date object

//     // Extract date components
//     const formattedDate = `${String(date.getMonth() + 1).padStart(2, '0')}/${String(date.getDate()).padStart(2, '0')}/${date.getFullYear()}`;

//     // Extract time components
//     const formattedTime = `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;

//     // Combine date and time
//     return `${formattedDate} at ${formattedTime}`;



// }

export const formatCreatedAt = (createdAt) => {
    // Convert createdAt to a Date object
    if (!createdAt.endsWith("Z") && !createdAt.includes("+")) {
        createdAt += "Z";
    }

    const date = new Date(createdAt);

    // Define options for EST formatting
    const options = {
        timeZone: "America/New_York",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false, // Optional: Use 24-hour format
    };

    // Use Intl.DateTimeFormat to format the date to EST
    const formatter = new Intl.DateTimeFormat("en-US", options);
    const parts = formatter.formatToParts(date);

    // Extract parts (e.g., month, day, year, hour, minute)
    const datePart = `${parts.find(p => p.type === "month").value}/${parts.find(p => p.type === "day").value}/${parts.find(p => p.type === "year").value}`;
    const timePart = `${parts.find(p => p.type === "hour").value}:${parts.find(p => p.type === "minute").value}`;

    // Combine and return the formatted date and time
    return `${datePart} at ${timePart}`;
};


/**
 * Create list item element for UI representation of fridge item.
 * @param list HTML list element to append fridge item to.
 * @param item object containing fridge item data.
 * @param inTrash checks if item is in trash or not.
 */
export const toListItem = (list, item, inTrash) => {
    const listItem = document.createElement('li');
    const escapeString = (str) => str.replace(/'/g, "\\'").replace(/"/g, '\\"');

    if (isExpired(item.expDate)) {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> <span class="${!inTrash ? `amt-num` : ''}" onclick="${!inTrash ? `enableEditMode(event, ${item.id}, '${item.uid}', '${escapeString(item.name)}', ${item.amount}, '${item.expDate}')` : ''}">${item.amount}</span></div> 
                        <div class="item-exp-date expired"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else if (isExpired(item.expDate, "today")) {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> <span class="${!inTrash ? `amt-num` : ''}" onclick="${!inTrash ? `enableEditMode(event, ${item.id}, '${item.uid}', '${escapeString(item.name)}', ${item.amount}, '${item.expDate}')` : ''}">${item.amount}</span></div>  
                        <div class="item-exp-date last-day"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong> <span class="${!inTrash ? `amt-num` : ''}" onclick="${!inTrash ? `enableEditMode(event, ${item.id}, '${item.uid}', '${escapeString(item.name)}', ${item.amount}, '${item.expDate}')` : ''}">${item.amount}</span></div> 
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
            const fridgeItems = await getUserItems() // ItemModel[]
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
 * Blocks unauthortized access to website.
 */
export const restrictPageContent = () => {
    if (!isLoggedIn()) {
        document.body.innerHTML = "";
        return;
    }
}

/**
 * Prevent user from going back to website if they logged out.
 */
export const redirectToHome = () => {
    if (!isLoggedIn()) {
        window.location.href = HOME_PAGE
    }
}

/**
 * Checks if user is logged in or not.
 * @returns 
 */
const isLoggedIn = () => localStorage.getItem("username") != null && localStorage.getItem("uid") != null

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