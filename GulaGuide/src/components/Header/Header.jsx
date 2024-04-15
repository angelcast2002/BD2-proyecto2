import React from "react"
import { LuLogOut } from "react-icons/lu"
import { navigate } from "../../store"
import style from "./header.module.css"

const handleClick = () => {
  navigate("/login")
}

export const Header = () => {
  return (
    <div className={style.mainContainer}>
      <div className={style.actions}>
        <a href="/editprofile">Perfil</a>
        <a href="/chat">Chat</a>
      </div>
      <div className={style.buttonLogoutMobile} onClick={handleClick}>
        <LuLogOut size={30} style={{ color: "#000" }} />
      </div>
    </div>
  )
}

export default Header
