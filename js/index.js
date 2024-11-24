// import { UserModel } from "./models/UserModel.js";

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
const logIn = (event) => {
    event.preventDefault();
    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("password").value.trim();

    const storedUsername = "orderbyrizz"// localStorage.getItem("username");
    const storedPassword = "anwica" // localStorage.getItem("password");


    if (storedUsername === username && storedPassword === password) {
        alert(`Welcome, ${username}!`);
        document.getElementById("loginform").style.display = "none";
        document.getElementById("createAccountForm").style.display = "none";
        document.getElementById("username").value = "";
        document.getElementById("password").value = "";
        document.getElementById("logoutSection").style.display = "flex";
        window.location.href = "fridge.html"
    } else {
        alert("Invalid username or password. Please try again.");
    }
};

/**Create Account Functionality*/
const createAccount = () => {
    const newUsername = document.getElementById("newUsername").value;
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (!newUsername || !newPassword || !confirmPassword) {
        alert("Please fill in all fields.");
        return;
    }

    if (newPassword !== confirmPassword) {
        alert("Passwords do not match. Please try again.");
        return;
    }

    // Store the new user details in localStorage
    localStorage.setItem("username", newUsername);
    localStorage.setItem("password", newPassword);

    alert("Account created successfully! Please log in.");
    showLoginForm();
};

// Log Out Functionality
const logOut = () => {
    alert("You have been logged out.");
    showLoginForm();
};