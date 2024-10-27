const logIn = (event) => {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const registered = document.getElementById("registered");
    if (!registered.checked) {
        createNewAccount(username, password);

        // do other logic and route them to next page
        return;
    }

    console.log(`User ${username} logged in with password ${password}.`);
}

/**
 * Register a new user in the database.
 */
const createNewAccount = (username, password) => {
    console.log(`New account created for ${username} with password ${password}.`);
}
