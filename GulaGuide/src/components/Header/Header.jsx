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
  console.log("role", role)
  console.log(user === "diner")
  return (
    <div className={style.mainContainer}>
      <div className={style.actions}>
        <a href="/edituser">Perfil</a>
        <a
          href="/recommendations"
          style={role === "Diner" ? { display: "block" } : { display: "none" }}
        >
          Recomendaciones
        </a>
        <a
          href="/createnodes"
          style={role === "Diner" ? { display: "none" } : { display: "block" }}
        >
          Agregar plato
        </a>
        <a
          href="/createnodes"
          style={role === "Diner" ? { display: "none" } : { display: "block" }}
        >
          Agregar parqueo
        </a>
      </div>
      <div className={style.buttonLogoutMobile} onClick={handleClick}>
        <LuLogOut size={30} style={{ color: "#000" }} />
      </div>
    </div>
  )
}

export default Header
