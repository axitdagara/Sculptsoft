"""
Simple RBAC demo (no FastAPI, no external libs).

This file keeps the same logic as the original RBAC.py but in a
very basic, beginner-friendly command-line program. It shows:
- users with roles
- role -> permissions mapping
- login (username/password)
- list/view/create/delete posts guarded by permissions
- admin-only user listing

Password for all sample users is: secret123

Run: python rbac_basic.py
"""

USERS_DB = {
    "alice": {"username": "alice", "email": "alice@example.com", "password": "secret123", "roles": ["admin"]},
    "bob":   {"username": "bob",   "email": "bob@example.com",   "password": "secret123", "roles": ["editor"]},
    "charlie": {"username": "charlie", "email": "charlie@example.com", "password": "secret123", "roles": ["viewer"]},
}

ROLE_PERMISSIONS = {
    "viewer": {"posts:read"},
    "editor": {"posts:read", "posts:write"},
    "admin":  {"posts:read", "posts:write", "posts:delete"},
}

POSTS_DB = [
    {"id": 1, "title": "Hello World", "body": "First post!", "author": "alice"},
    {"id": 2, "title": "FastAPI Tips", "body": "Use Depends().", "author": "bob"},
]


def authenticate_user(username: str, password: str):
    """Return user dict if username/password match, else None."""
    user = USERS_DB.get(username)
    if not user:
        return None
    if user["password"] != password:
        return None
    # Return a lightweight "token" (just a dict) with username and roles
    return {"username": user["username"], "roles": list(user["roles"])}


def has_permission(user: dict, permission: str) -> bool:
    """Check if any of the user's roles grant the permission."""
    user_roles = user.get("roles", [])
    for r in user_roles:
        perms = ROLE_PERMISSIONS.get(r, set())
        if permission in perms:
            return True
    return False


def is_admin(user: dict) -> bool:
    return "admin" in user.get("roles", [])


def list_posts(user: dict):
    if not has_permission(user, "posts:read"):
        print("403 Forbidden: aapke paas posts dekhne ki permission nahi hai.")
        return
    print("\n--- Posts ---")
    for p in POSTS_DB:
        print(f"{p['id']}. {p['title']} (by {p['author']})")
    print("-------------\n")


def view_post(user: dict):
    if not has_permission(user, "posts:read"):
        print("403 Forbidden: posts:read required")
        return
    try:
        pid = int(input("Enter post id: "))
    except ValueError:
        print("Invalid id")
        return
    post = next((p for p in POSTS_DB if p["id"] == pid), None)
    if not post:
        print("Post not found")
        return
    print(f"\nTitle: {post['title']}\nAuthor: {post['author']}\nBody: {post['body']}\n")


def create_post(user: dict):
    if not has_permission(user, "posts:write"):
        print("403 Forbidden: posts:write required")
        return
    title = input("Title: ")
    body = input("Body: ")
    new_id = max((p["id"] for p in POSTS_DB), default=0) + 1
    new_post = {"id": new_id, "title": title, "body": body, "author": user["username"]}
    POSTS_DB.append(new_post)
    print(f"Post created with id {new_id}")


def delete_post(user: dict):
    if not has_permission(user, "posts:delete"):
        print("403 Forbidden: posts:delete required")
        return
    try:
        pid = int(input("Enter post id to delete: "))
    except ValueError:
        print("Invalid id")
        return
    global POSTS_DB
    post = next((p for p in POSTS_DB if p["id"] == pid), None)
    if not post:
        print("Post not found")
        return
    POSTS_DB = [p for p in POSTS_DB if p["id"] != pid]
    print(f"Post {pid} deleted by {user['username']}")


def list_users(user: dict):
    if not is_admin(user):
        print("403 Forbidden: admin role required")
        return
    print("\n--- Users ---")
    for u in USERS_DB.values():
        print(f"{u['username']} | {u['email']} | roles: {', '.join(u['roles'])}")
    print("-------------\n")


def show_menu(user: dict):
    while True:
        print("Choose action:")
        print("1. List posts (posts:read)")
        print("2. View post (posts:read)")
        print("3. Create post (posts:write)")
        print("4. Delete post (posts:delete)")
        print("5. My info")
        print("6. List users (admin only)")
        print("0. Logout / Exit")
        choice = input("Enter number: ")
        if choice == "1":
            list_posts(user)
        elif choice == "2":
            view_post(user)
        elif choice == "3":
            create_post(user)
        elif choice == "4":
            delete_post(user)
        elif choice == "5":
            print(f"Username: {user['username']}, roles: {', '.join(user['roles'])}")
        elif choice == "6":
            list_users(user)
        elif choice == "0":
            print("Logged out. Bye!")
            break
        else:
            print("Unknown choice, try again.")


def main():
    print("Welcome to simple RBAC demo")
    print("Sample users: alice(admin), bob(editor), charlie(viewer). Password: secret123")
    username = input("Username: ")
    password = input("Password: ")
    user = authenticate_user(username.strip(), password.strip())
    if not user:
        print("Login failed: incorrect username or password")
        return
    print(f"Hello {user['username']}! Your roles: {', '.join(user['roles'])}")
    show_menu(user)


if __name__ == "__main__":
    main()
