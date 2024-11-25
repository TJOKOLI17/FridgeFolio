// import { UserModel } from "./models/UserModel.js";

import { UserCreate, UserResponse } from "./models/UserModels.js";
import { getUserByPassword, getUserById, createNewUser } from "./services/UserService.js";


/**Show the Create Account form*/
const showCreateAccountForm = () => {
    document.getElementById("loginform").style.display = "none";
    document.getElementById("createAccountForm").style.display = "flex";
};

/**Show the Login form*/
const showLoginForm = () => {
    document.getElementById("createAccountForm").style.display = "none";
    document.getElementById("loginform").style.display = "flex";
    document.getElementById("logoutSection").style.display = "none";
};

/**Log In Functionality*/
// const logIn = (event) => {
//     event.preventDefault();
//     let username = document.getElementById("username").value.trim();
//     let password = document.getElementById("password").value.trim();

//     // const storedUsername = "orderbyrizz"// localStorage.getItem("username");
//     // const storedPassword = "anwica" // localStorage.getItem("password");


//     if (storedUsername === username && storedPassword === password) {
//         alert(`Welcome, ${username}!`);
//         document.getElementById("loginform").style.display = "none";
//         document.getElementById("createAccountForm").style.display = "none";
//         document.getElementById("username").value = "";
//         document.getElementById("password").value = "";
//         document.getElementById("logoutSection").style.display = "flex";
//         window.location.href = "fridge.html"
//     } else {
//         alert("Invalid username or password. Please try again.");
//     }
// };

/**Log in account functionality*/
const logIn = async () => {
    try {
        let username = document.getElementById("username").value.trim();
        let password = document.getElementById("password").value.trim();

        if (username === "" || password === "") {
            window.alert("Please fill out all fields.")
            return;
        }

        const user = await getUserByPassword(new UserCreate(username, password))

        localStorage.setItem("username", user.username)
        localStorage.setItem("uid", String(user.uid))
        localStorage.setItem("createdAt", String(user.createdAt))
        window.location.href = "fridge.html"
    } catch (error) {
        window.alert(error.message)
    }


}

/**Create account functionality*/
const createAccount = async () => {
    try {
        const newUsername = document.getElementById("newUsername").value.trim();
        const newPassword = document.getElementById("newPassword").value.trim();
        const confirmPassword = document.getElementById("confirmPassword").value.trim();

        // console.log(newPassword);
        // console.log(confirmPassword);
        // console.log();

        if (username === "" || password === "" || confirmPassword === "") {
            window.alert("Please fill out all fields.")
            return;
        }

        if (newPassword !== confirmPassword) {
            window.alert("Passwords do not match");
            return;
        }

        const newUser = await createNewUser(new UserCreate(newUsername, newPassword))
        localStorage.setItem("username", newUser.username)
        localStorage.setItem("uid", String(newUser.uid))
        localStorage.setItem("createdAt", String(newUser.createdAt))
        window.location.href = "fridge.html"
    } catch (error) {
        window.alert(error.message)
    }
};

window.logIn = logIn
window.showLoginForm = showLoginForm
window.createAccount = createAccount
window.showCreateAccountForm = showCreateAccountForm
