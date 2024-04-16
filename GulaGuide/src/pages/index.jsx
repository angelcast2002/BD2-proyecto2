import { useStoreon } from "storeon/react"
import { routerKey } from "@storeon/router"
import React from "react"
import Home from "./Home/Home"
import LogIn from "./LogIn/LogIn"
import SignUp from "./SignUp/SignUp"
import EditUser from "./EditUser/EditUser"
import Recommendations from "./Recommendations/Recommendations"
import SetSettings from "./SetSettings/SetSettings"
import ResInfo from "./ResInfo/ResInfo"

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
    case "edituser":
      Component = <EditUser />
      break
    case "recommendations":
      Component = <Recommendations />
      break
    case "setsettings":
      Component = <SetSettings />
      break
    case "resinfo":
      Component = <ResInfo />
      break
    default:
      Component = <h1>404 Error</h1>
  }

  return <main>{Component}</main>
}

export default Page
