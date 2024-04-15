import React, { useState } from "react"
import { FaBars, FaTimes } from "react-icons/fa"
import { LuLogOut } from "react-icons/lu"
import styles from "./HeaderHome.module.css"
import { navigate } from "../../store"

const HeaderHome = () => {
  const [showNavbar, setShowNavbar] = useState(false)

  const handleShowNavbar = () => {
    setShowNavbar(!showNavbar)
  }

  const renderActions = () => {
    return (
      <div className="actions">
        <div className={styles.actionlinks}>
          <a href="/login" className={styles.buttonlogin}>
            Iniciar sesión
          </a>
          <a href="/signup">Registrarse</a>
        </div>
      </div>
    )
  }

  const handleHome = () => {
    navigate("/")
  }

  return (
    <nav className={styles.navbar}>
      <div className={styles.container}>
        <div className={styles.logoheader}>
          <button className={styles.buttonlogo} onClick={handleHome} type="button">
            <img src="/images/Ue_2.svg" alt="Logo" />
          </button>
        </div>
        <div className={styles.menuicon} onClick={handleShowNavbar}>
          {showNavbar ? (
            <FaTimes size={30} style={{ color: "#000" }} />
          ) : (
            <FaBars size={30} style={{ color: "#000" }} />
          )}
        </div>
        <div
          className={styles.navelements + " " + (showNavbar && styles.active)}
        >
          {renderActions()}
        </div>
      </div>
    </nav>
  )
}

export default HeaderHome
