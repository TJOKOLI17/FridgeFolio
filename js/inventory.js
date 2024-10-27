import { getItems, addItem, updateItem, deleteItem } from "./services/itemService.js";

const itemSubmit = document.getElementById("item-submit")

// itemSubmit.addEventListener('submit', async (event) => {
//     event.preventDefault();
//     const name = document.getElementById("name").value;
//     const amount = document.getElementById("amount").value;
//     const expYear = Number(document.getElementById("expYear").value);
//     const expMonth = Number(document.getElementById("expMonth").value);
//     const expDay = Number(document.getElementById("expDay").value);
//     const expDate = `${expYear}/${expMonth}/${expDay}`

//     if (typeof (expDay) !== "number" || typeof (expMonth) !== "number" || typeof (expYear) !== "number") {
//         window.alert("Please enter valid numbers for date information")
//     } else {
//         try {
//             const newItem = await addItem({
//                 name: name,
//                 amount: amount,
//                 expDate: expDate
//             })

//             console.log(newItem.name, newItem.amount, newItem.expDate);
//             itemSubmit.reset()
//         } catch (error) {
//             window.alert(error)
//         }

//     }
// })

itemSubmit.addEventListener('submit', async (event) => {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const amount = document.getElementById("amount").value;
    const expDate = document.getElementById("expDate").value.replaceAll('-', '/')

    try {
        const newItem = await addItem({
            name: name,
            amount: amount,
            expDate: expDate
        })

        console.log(newItem.name, newItem.amount, newItem.expDate);
        itemSubmit.reset()
    } catch (error) {
        window.alert(error)
    }
})
