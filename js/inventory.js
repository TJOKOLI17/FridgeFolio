import { addItem } from "./services/itemService.js";
import { isExpired, redirectToHome, restrictPageContent } from "./services/sharedService.js";

const itemSubmit = document.getElementById("item-submit")

itemSubmit.addEventListener('submit', async (event) => {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const amount = document.getElementById("amount").value;
    const expDate = document.getElementById("expDate").value.replaceAll('-', '/')

    try {
        const newItem = await addItem({
            name: name,
            uid: Number(localStorage.getItem("uid")),
            amount: amount,
            expDate: expDate
        })

        addToRecentlyAdded(newItem)
        itemSubmit.reset()
    } catch (error) {
        window.alert(error)
    }
});

function addToRecentlyAdded(newItem) {
    const recentlyAdded = document.getElementById('recently-added');
    recentlyAdded.appendChild(toRecentlyAddedListItem(newItem))
    recentlyAdded.appendChild(document.createElement('br'));;
}

const toRecentlyAddedListItem = (item) => {
    const recentlyAdded = document.getElementById('recentlyAdded');
    // Create the list item
    const listItem = document.createElement('li');

    if (isExpired(item.expDate)) {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong>${item.amount}</div>
                        <div class="item-exp-date expired"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else if (isExpired(item.expDate, "today")) {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong>${item.amount}</div> 
                        <div class="item-exp-date last-day"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    } else {
        listItem.innerHTML = `
                    <div class="item-model-container">
                        <div class="item-name"><strong>Name: </strong> ${item.name}</div>
                        <div class="item-amount"><strong> Amount: </strong>${item.amount}</div>
                        <div class="item-exp-date"><strong> Expiration Date: </strong> ${new Date(item.expDate).toDateString()}</div>
                    </div>`;
    }

    listItem.classList.add('list-item');

    return listItem
}

restrictPageContent()
redirectToHome()
