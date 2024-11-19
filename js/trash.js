import { ItemModel } from "./models/ItemModel.js";
import { get_deleted_items } from "./services/itemService.js";
import { isExpired } from "./services/helperService.js";

const populateDeletedList = async () => {
    try {
        const deletedList = document.getElementById('trash-list');
        deletedList.replaceChildren();
        const deletedFridgeItems = await get_deleted_items()
        deletedFridgeItems.forEach((deletedFridgeItem) => {
            toListItem(deletedFridgeItem);
        })
    } catch (error) {
        console.error(error);
    }
}

const toListItem = (item) => {
    const deletedList = document.getElementById('trash-list');
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

    deletedList.appendChild(listItem);
    deletedList.appendChild(document.createElement('br'));
}

populateDeletedList()