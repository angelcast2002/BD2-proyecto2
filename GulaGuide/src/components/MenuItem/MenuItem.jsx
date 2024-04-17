import React from "react"
import style from "./MenuItem.module.css"

const MenuItem = ({ name, description, avg_price }) => {
  return (
    <div className={style.menuItemContainer}>
      <strong>{name + " | " + avg_price}</strong> {" "}
      <p>{description}</p>
    </div>
  )
}

export default MenuItem