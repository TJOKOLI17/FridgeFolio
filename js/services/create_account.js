const createAccount = (event) => {
    event.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirmPassword").value.trim();

    if (!username || !password || !confirmPassword) {
        alert("Please fill in all fields.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match. Please try again.");
        return;
    }

    console.log(`New account created for ${username} with password ${password}.`);
    alert("Account successfully created! Redirecting to login page...");
    window.location.href = "index.html"; 
}