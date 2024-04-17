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
  ["/addvisit/*", (restaurant_id) => ({ page: "addvisit", props: { restaurant_id }})],
  ["/adddish", () => ({ page: "adddish" })],
  ["/addparking", () => ({ page: "addparking" })],
  ["/dinerondish/*", (id) => ({ page: "dinerondish", props: { id }})],
  ["/homeadmin", () => ({ page: "homeadmin" })]
])
