import React from "react"
import style from "./MenuItem.module.css"

const MenuItem = ({ name, description, price }) => {
  return (
    <div className={style.menuItemContainer}>
      <strong>{name}</strong> {" "}
      <p>{description}</p>
      <p>{price}</p>
    </div>
  )
}

export default MenuItem