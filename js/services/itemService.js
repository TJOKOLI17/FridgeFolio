import { ItemModel } from "../models/ItemModel.js";
import { itemAPIKey } from "./keys.js";


export const getItems = async () => {
    try {
        let fridge = [];
        const response = await fetch(itemAPIKey);
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

export const get_deleted_items = async () => {
    try {
        let trash = [];
        // const response = await fetch(`${itemAPIKey}/deleted`, {
        //     method: 'GET',
        // });
        const response = await fetch(`${itemAPIKey}/deleted`);
        if (!response.ok) {
            throw new Error("Error in fetching trash can")
        }
        const allDeletedItems = await response.json()
        for (let item of allDeletedItems) {
            trash.push(new ItemModel(item.id, item.name, item.amount, item.expDate))
        }
        return trash
    } catch (error) {
        console.error(error);
    }
}

export const addItem = async (newItem) => {
    try {
        const response = await fetch(itemAPIKey, {
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

        return new ItemModel(
            currentItem.id,
            currentItem.name,
            currentItem.amount,
            currentItem.expDate
        );
    } catch (error) {
        throw new Error(error)
    }
}

export const updateItem = async (modifiedItem) => {
    try {
        const response = await fetch(itemAPIKey, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(modifiedItem),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const updatedItem = await response.json();

        return new ItemModel(
            updatedItem.id,
            updatedItem.name,
            updatedItem.amount,
            updatedItem.expDate
        )
    } catch (error) {
        throw new Error(error)
    }

}

export const deleteItem = async (item) => {
    try {
        await fetch(`${itemAPIKey}/${item.id}`, {
            method: 'DELETE',
        });
    } catch (error) {
        throw new Error(error)
    }
}