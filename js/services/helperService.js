export const isExpired = (date, check = null) => {
    const today = new Date(String(new Date().toLocaleDateString()))

    if (check == "today") {
        const todayAsString = `${new Date().getFullYear()}/${new Date().getMonth() + 1}/${new Date().getDate()}`
        return date === todayAsString
    }

    return new Date(date) < today
}