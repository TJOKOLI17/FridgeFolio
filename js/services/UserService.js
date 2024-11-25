import { UserCreate, UserResponse } from "../models/UserModels.js";
import { SignInError, SignUpError } from "../errors/Errors.js";
import { userAPIKey } from "./keys.js";
import { formatCreatedAt } from "./sharedService.js";


/**
 * 
 * @param user user to be retrieved from the database.
 * @returns {Promise<UserResponse>} user of the currently logged in account. 
 */
export const getUserByPassword = async (user) => {
    const username = user.username
    const password = user.password
    try {
        const response = await fetch(`${userAPIKey}/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new SignInError(errorData.detail)
        }


        const foundUser = await response.json();

        foundUser.CreatedAt = formatCreatedAt(foundUser.CreatedAt)

        return new UserResponse(
            foundUser.uid,
            foundUser.username,
            foundUser.CreatedAt
        );
    } catch (error) {
        if (error instanceof SignInError) {
            throw new SignInError(error.message)
        }

        throw new Error(`Unexpected error while logging in: ${error.message}`);
    }
}

export const getUserById = async (user_id) => {
    try {
        const response = await fetch(`${userAPIKey}/${user_id}`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new SignInError(errorData.detail)
            // console.error("Error:", errorData.detail); // Log the error detail
            // alert(errorData.detail); // Show an alert to the user
            // return;
        }

        foundUser = await response.json();

        return new UserResponse(
            foundUser.uid,
            foundUser.username,
            foundUser.createdAt
        );
    } catch (error) {
        if (error instanceof SignInError) {
            throw new SignInError(error.message)
        }

        throw new Error(`Unexpected error while logging in ${error.message}`);
    }

}


/**
 * @param user new user to be created in the database.
 * @returns {Promise<UserResponse>} new user of the currently logged in account.
 */
export const createNewUser = async (user) => {
    try {
        const response = await fetch(userAPIKey, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(user),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new SignUpError(errorData.detail)
        }


        const newUser = await response.json();

        newUser.CreatedAt = formatCreatedAt(newUser.CreatedAt)

        return new UserResponse(
            newUser.uid,
            newUser.username,
            newUser.CreatedAt
        );
    } catch (error) {
        if (error instanceof SignUpError) {
            throw new SignUpError(error.message)
        }

        throw new Error(`Unexpected error while logging in: ${error.message}`);
    }
}