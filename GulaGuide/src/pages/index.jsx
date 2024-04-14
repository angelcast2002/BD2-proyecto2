import { useStoreon } from "storeon/react"
import { routerKey } from "@storeon/router"
import React from "react"

const Page = () => {
  const { [routerKey]: route } = useStoreon(routerKey)

  let Component = null
  switch (route.match.page) {
    case "home":
      Component = <h1>Home</h1>
      break
    default:
      Component = <h1>404 Error</h1>
  }

  return <main>{Component}</main>
}

export default Page
