import { redirectToHome } from "./services/sharedService.js";

// Log Out Functionality
const logOut = () => {
    // user = await getUserById(user_id);
    localStorage.removeItem("username")
    localStorage.removeItem("uid")
    window.location.href = "index.html"
};

window.logOut = logOut

redirectToHome()