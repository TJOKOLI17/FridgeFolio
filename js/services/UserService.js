import { UserCreate, UserResponse } from "../models/UserModels.js";
import { SignInError } from "../errors/SignInError.js";
import { userAPIKey } from "./keys.js";


export const getUserByPassword = async (user) => {
    const username = user.username
    const password = user.password
    try {
        const response = await fetch(`${userAPIKey}/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new SignInError("kill yourself")
            // console.error("Error:", errorData.detail); // Log the error detail
            // alert(errorData.detail); // Show an alert to the user
            // return;
        }

        console.log(`RESPONSE: ${response}`)

        const foundUser = await response.json();

        return new UserResponse(
            foundUser.uid,
            foundUser.username,
            foundUser.createdAt
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