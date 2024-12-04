import { getUserDeletedItems } from "./services/itemService.js";
import { toListItem, redirectToHome, restrictPageContent } from "./services/sharedService.js";

const populateDeletedList = async () => {
    try {
        const deletedList = document.getElementById('trash-list');
        deletedList.replaceChildren();
        const deletedFridgeItems = await getUserDeletedItems()
        deletedFridgeItems.forEach((deletedFridgeItem) => {
            deletedList.append(toListItem(deletedList, deletedFridgeItem, true));
            deletedList.appendChild(document.createElement('br'));
        })
    } catch (error) {
        console.error(error);
    }
}

restrictPageContent()
redirectToHome()
populateDeletedList()