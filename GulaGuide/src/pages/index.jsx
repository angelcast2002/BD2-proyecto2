import { useStoreon } from "storeon/react"
import { routerKey } from "@storeon/router"
import React from "react"
import Home from "./Home/Home"
import LogIn from "./LogIn/LogIn"
import SignUp from "./SignUp/SignUp"

const Page = () => {
  const { [routerKey]: route } = useStoreon(routerKey)

  let Component = null
  switch (route.match.page) {
    case "home":
      Component = <Home />
      break
    case "login":
      Component = <LogIn />
      break
    case "signup":
      Component = <SignUp />
      break
    default:
      Component = <h1>404 Error</h1>
  }

  return <main>{Component}</main>
}

export default Page
