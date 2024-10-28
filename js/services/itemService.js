import { ItemModel } from "../models/ItemModel.js";
import { apiKey } from "./key.js";


export const getItems = async () => {
    try {
        let fridge = [];
        const response = await fetch(apiKey);
        if (!response.ok) {
            throw new Error("Error in fetching fridge items")
        }
        const allItems = await response.json()
        for (let item of allItems) {
            fridge.push(new ItemModel(item.id, item.name, item.amount, item.expDate))
        }
        return fridge
    } catch (error) {
        console.error(error);

    }
}

export const addItem = async (newItem) => {
    try {
        const response = await fetch(apiKey, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newItem),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const currentItem = await response.json();
        console.log('Success:', currentItem);

        return new ItemModel(
            currentItem.id,
            currentItem.name,
            currentItem.amount,
            currentItem.expDate
        )
    } catch (error) {
        throw new Error(error)
    }
}

export const updateItem = async (id) => {
}

export const deleteItem = async (item) => {
    try {
        await fetch(`${apiKey}/${item.id}`, {
            method: 'DELETE',
        });
    } catch (error) {
        throw new Error(error)
    }
}