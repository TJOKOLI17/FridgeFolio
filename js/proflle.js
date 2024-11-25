// Log Out Functionality
const logOut = () => {
    // user = await getUserById(user_id);
    localStorage.removeItem("username")
    localStorage.removeItem("uid")
    window.location.href = "index.html"
};