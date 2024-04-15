import React from "react"
import style from "./Button.module.css"

const Button = ({ text, onClick, size }) => {
  return (
    <button
      className={style.button}
      onClick={onClick}
      style={{ width: size ? size : null }}
    >
      {text}
    </button>
  )
}

export default Button
