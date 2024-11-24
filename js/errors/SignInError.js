export class SignInError extends Error {
    constructor(message) {
        super(message)
        this.name = "SignInError"
    }
}

