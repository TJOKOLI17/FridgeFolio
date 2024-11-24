import { ItemModel } from "./models/ItemModel.js";
import { get_deleted_items } from "./services/itemService.js";
import { isExpired, toListItem } from "./services/sharedService.js";

const populateDeletedList = async () => {
    try {
        const deletedList = document.getElementById('trash-list');
        deletedList.replaceChildren();
        const deletedFridgeItems = await get_deleted_items()
        deletedFridgeItems.forEach((deletedFridgeItem) => {
            deletedList.append(toListItem(deletedList, deletedFridgeItem, true));
            deletedList.appendChild(document.createElement('br'));
        })
    } catch (error) {
        console.error(error);
    }
}

populateDeletedList()