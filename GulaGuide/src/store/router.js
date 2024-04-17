import { createRouter } from "@storeon/router"

export default createRouter([
  ["/", () => ({ page: "home" })],
  ["/login", () => ({ page: "login" })],
  ["/signup", () => ({ page: "signup" })],
  ["/edituser", () => ({ page: "edituser" })],
  ["/recommendations", () => ({ page: "recommendations" })],
  ["/setsettings", () => ({ page: "setsettings" })],
  ["/resinfo/*", (id) => ({ page: "resinfo", props: { id } })],
  ["/dishinfo", () => ({ page: "dishinfo" })],
  ["/addvisit", () => ({ page: "addvisit" })],
])
