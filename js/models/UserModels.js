/**
 * Shared attributes of a User.
 */
class UserBase {
    constructor(username) {
        this.username = username;
    }
}

/**
 * Attributes required for creating a new User.
 */
export class UserCreate extends UserBase {
    constructor(username, password) {
        super(username)
        this.password = password;
    }
}

/**
 * Attributes returned when a User is retrieved.
 */
export class UserResponse extends UserBase {
    constructor(uid, username, createdAt) {
        super(username)
        this.uid = uid
        this.createdAt = createdAt;
    }
}