const logIn = (event) => {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const registered = document.getElementById("registered");

    if (!username || !password) {
        alert("Please fill in all fields.");
        return;
    }

    if (!registered.checked) {
        alert("Please click 'Create Account' to register.");
                return;
        }

        console.log(`User ${username} logged in with password ${password}.`);

    };
    const redirectToCreateAccount = () => {
        window.location.href = "create_account.html"; // Redirects to account creation page
    };

    

/**
 * Register a new user in the database.
 * @param username - user's name
 * @param password - user's password
 */

const createNewAccount = (username, password) => {
    console.log(`New account created for ${username} with password ${password}.`);
    alert("Account successfully created! Please log in.");
}
