import { StoreContext } from "storeon/react"
import store from "@store"
import React from "react"
import Page from "./pages/index"
import "./App.css"

const App = () => {
  return (
    <StoreContext.Provider value={store}>
      <div className="App">
        <Page />
      </div>
    </StoreContext.Provider>
  )
}

export default App
