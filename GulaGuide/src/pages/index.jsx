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
import DishInfo from "./DishInfo/DishInfo"
import AddVisit from "./AddVisit/AddVisit"
import AddDish from "./AddDish/AddDish"
import AddParking from "./AddParking/AddParking"
import DinerOnDish from "./DinerOnDish/DinerOnDish"
import HomeAdmin from "./HomeAdmin/HomeAdmin"

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
      Component = <ResInfo id={route.match.props.id} />
      break
    case "dishinfo":
      Component = <DishInfo />
      break
    case "addvisit":
      Component = <AddVisit restaurant_id={route.match.props.restaurant_id}/>
      break
    case "adddish":
      Component = <AddDish />
      break
    case "addparking":
      Component = <AddParking />
      break
    case "dinerondish":
      Component = <DinerOnDish id={route.match.props.id}/>
      break
    case "homeadmin":
      Component = <HomeAdmin />
      break
    default:
      Component = <h1>404 Error</h1>
  }

  return <main>{Component}</main>
}

export default Page
