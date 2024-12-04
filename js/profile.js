import { redirectToHome, restrictPageContent } from "./services/sharedService.js";
import { deleteUser } from "./services/UserService.js";

const userId = document.getElementById("user-id");
const usernname = document.getElementById("username");
const userCreatedAt = document.getElementById("user-createdAt");

username.textContent = `Username: ${localStorage.getItem("username")}`
userId.textContent = `User ID: ${localStorage.getItem("uid")}`
userCreatedAt.textContent = `Acounted Created: ${localStorage.getItem("createdAt")}`


// Log Out Functionality
const logOut = () => {
    // user = await getUserById(user_id);
    localStorage.removeItem("username")
    localStorage.removeItem("uid")
    localStorage.removeItem("createdAt")
    window.location.href = "index.html"
};

const deleteUserAndLogOut = async () => {
    if (window.confirm("Are you sure? \nThis is a permanent action and cannot be undone.")) {
        await deleteUser()
        logOut()
    } else {
        return;
    }
}

window.logOut = logOut
window.deleteUserAndLogOut = deleteUserAndLogOut



restrictPageContent()
redirectToHome()