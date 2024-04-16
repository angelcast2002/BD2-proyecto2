import { createRouter } from "@storeon/router"

export default createRouter([
  ["/", () => ({ page: "home" })],
  ["/login", () => ({ page: "login" })],
  ["/signup", () => ({ page: "signup" })]
  ["/edituser", () => ({ page: "edituser" })]
])
