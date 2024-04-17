import React from "react"
import { LuLogOut } from "react-icons/lu"
import { navigate } from "../../store"
import style from "./header.module.css"
import { useStoreon } from "storeon/react"

const handleClick = () => {
  navigate("/login")
}

export const Header = () => {
  const { user } = useStoreon("user")
  const { role } = user

  return (
    <div className={style.mainContainer}>
      <div className={style.actions}>
        <a href="/edituser">Perfil</a>
        <a href="/recommendations" style={role === "diner" ? {display: 'none'} : {}}>Recomendaciones</a>
        <a href="/createnodes" style={role === "diner" ? {} : {display: 'none'}}>Crear entidades</a>
      </div>
      <div className={style.buttonLogoutMobile} onClick={handleClick}>
        <LuLogOut size={30} style={{ color: "#000" }} />
      </div>
    </div>
  )
}

export default Header
