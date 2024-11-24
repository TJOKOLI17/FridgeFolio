class UserBase {
    constructor(username) {
        this.username = username;
    }
}

export class UserCreate extends UserBase {
    constructor(username, password) {
        super(username)
        this.password = password;
    }
}

export class UserResponse extends UserBase {
    constructor(uid, username, createdAt) {
        super(username)
        this.uid = uid
        this.createdAt = createdAt;
    }
}