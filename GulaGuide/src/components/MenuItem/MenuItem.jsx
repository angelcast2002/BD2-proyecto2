import React from "react"
import style from "./MenuItem.module.css"

const MenuItem = ({ name, description, avg_price, onClick }) => {
  return (
    <div className={style.menuItemContainer} onClick={onClick}>
      <strong>{name + " | " + avg_price}</strong> {" "}
      <p>{description}</p>
    </div>
  )
}

export default MenuItem