export class SignInError extends Error {
    constructor(message) {
        super(message)
        this.name = "SignInError"
    }
}

export class SignUpError extends Error {
    constructor(message) {
        super(message)
        this.name = "SignUpError"
    }
}

